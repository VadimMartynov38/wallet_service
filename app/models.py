from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import String, Integer, DateTime

class Base(DeclarativeBase):
    pass

class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    balance: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
