from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Wallet


async def apply_operation(
    session: AsyncSession, wallet_id: str, op_type: str, amount: int
) -> int:
    # Находим кошелёк и блокируем строку до конца транзакции
    stmt = select(Wallet).where(Wallet.id == wallet_id).with_for_update()
    result = await session.execute(stmt)
    wallet = result.scalars().one_or_none()
    if not wallet:
        raise ValueError("Wallet not found")

    if op_type == "DEPOSIT":
        wallet.balance += amount
    elif op_type == "WITHDRAW":
        if wallet.balance < amount:
            raise ValueError("Insufficient funds")
        wallet.balance -= amount

    await session.commit()
    return wallet.balance
