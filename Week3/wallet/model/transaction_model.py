from pydantic import BaseModel ,Field
from typing import Optional, Literal
from datetime import datetime
from decimal import Decimal

class TransactionModel(BaseModel):
    id: Optional[int] = Field(default=None)
    sender_id: Optional[int]
    receiver_id: Optional[int]
    datetime: Optional[datetime] = None
    type: Literal['deposit', 'withdraw', 'transfer']
    amount: Decimal
    status: Literal['pending', 'failed', 'completed'] = 'pending'
    remarks: str
