from enum import Enum

from pydantic import BaseModel, Field


class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class WalletOperationRequest(BaseModel):
    operation_type: OperationType
    amount: int = Field(..., gt=0)


class WalletResponse(BaseModel):
    id: str
    balance: int


class WalletCreate(BaseModel):
    id: str
