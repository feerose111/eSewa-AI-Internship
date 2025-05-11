from pydantic import BaseModel, Field
from typing import Literal, Optional
from decimal import Decimal

class UserModel(BaseModel):
    id: Optional[int] = Field(default=None)  # Auto-incremented by DB
    acc_num: str
    user_name: str
    user_type: Literal['basic', 'premium', 'business'] = 'basic'
    balance: Decimal = Decimal("0.00")
