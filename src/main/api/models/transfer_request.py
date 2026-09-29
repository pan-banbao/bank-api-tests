from src.main.api.models.base_model import BaseModel
from decimal import Decimal

class TransferRequest(BaseModel):
    fromAccountId: int
    toAccountId: int
    amount: float