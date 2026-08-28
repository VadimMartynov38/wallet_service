import os
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.models import Base

from app.config import settings
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite+aiosqlite:///tests/test.db")
settings.database_url = TEST_DATABASE_URL

from app.main import app
from app.db import get_session

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)

@pytest.fixture(scope="session")
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session(setup_db):
    async_session = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with async_session() as session:
        yield session

@pytest.fixture
async def client(db_session):
    original_override = app.dependency_overrides.get(get_session)

    async def override_get_session():
        return db_session

    app.dependency_overrides[get_session] = override_get_session

    from httpx import AsyncClient, ASGITransport
    async with AsyncClient(transport=ASGITransport(app=app),base_url="http://test") as c:
        yield c

    if original_override is not None:
        app.dependency_overrides[get_session] = original_override
    else:
        del app.dependency_overrides[get_session]
