from pydantic import BaseModel ,Field
from typing import Optional, Literal
from datetime import datetime
from decimal import Decimal

class TransactionModel(BaseModel):
    id: Optional[int] = Field(default=None)
    sender_id: Optional[int] = None
    receiver_id: Optional[int] = None
    datetime: Optional[datetime] = None
    tx_type: Literal['deposit', 'withdraw', 'transfer', 'balance']
    amount: Decimal
    status: Literal['pending', 'failed', 'completed'] = 'pending'
    remarks: str
