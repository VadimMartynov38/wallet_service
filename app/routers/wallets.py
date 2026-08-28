import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.operations import apply_operation
from app.schemas import WalletOperationRequest, WalletResponse, WalletCreate
from app.models import Wallet
from sqlalchemy import select

router = APIRouter(tags=["wallets"])

@router.post("/api/v1/wallets", response_model=WalletResponse, status_code=status.HTTP_201_CREATED)
async def create_wallet(session: AsyncSession = Depends(get_session)):
    wallet_id = str(uuid.uuid4())
    wallet = Wallet(id=wallet_id, balance=0)
    session.add(wallet)
    await session.flush()
    await session.refresh(wallet)
    await session.commit()
    return WalletResponse(id=wallet.id, balance=wallet.balance)

@router.post("/api/v1/wallets/{wallet_uuid}/operation")
async def wallet_operation(
    wallet_uuid: str,
    payload: WalletOperationRequest,
    session: AsyncSession = Depends(get_session),
):
    try:
        new_balance = await apply_operation(session, wallet_uuid, payload.operation_type.value, payload.amount)
        return {"balance": new_balance}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/api/v1/wallets/{wallet_uuid}", response_model=WalletResponse)
async def get_wallet(
    wallet_uuid: str,
    session: AsyncSession = Depends(get_session),
):
    stmt = select(Wallet).where(Wallet.id == wallet_uuid)
    result = await session.execute(stmt)
    wallet = result.scalars().one_or_none()
    if not wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")
    return WalletResponse(id=wallet.id, balance=wallet.balance)
