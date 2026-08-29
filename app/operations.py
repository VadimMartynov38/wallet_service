from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Wallet


async def apply_operation(
    session: AsyncSession, wallet_id: str, op_type: str, amount: int
) -> int:
    stmt = select(Wallet).where(Wallet.id == wallet_id).with_for_update()
    result = await session.execute(stmt)
    wallet = result.scalars().one_or_none()
    if not wallet:
        raise ValueError("Wallet not found")

    current_balance = cast(int, wallet.balance)
    if op_type == "DEPOSIT":
        current_balance += amount
    elif op_type == "WITHDRAW":
        if current_balance < amount:
            raise ValueError("Insufficient funds")
        current_balance -= amount

    wallet.balance = current_balance
    await session.commit()
    return current_balance
