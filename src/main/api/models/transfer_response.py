from src.main.api.models.base_model import BaseModel
from decimal import Decimal

class TransferResponse(BaseModel):
    fromAccountId: int
    toAccountId: int
    fromAccountIdBalance: float