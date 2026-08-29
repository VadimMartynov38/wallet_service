from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .config import settings

if not settings.database_url:
    raise RuntimeError("DATABASE_URL is not set")

engine = create_async_engine(settings.database_url, echo=False, future=True)
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
