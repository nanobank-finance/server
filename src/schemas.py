from typing import Union
from pydantic import BaseModel
from enum import Enum

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

class LoanApplication(BaseModel):
    name: str

class CheckType(Enum):
    CREDIT_CHECK: 1
    PROOF_OF_INCOME_CHECK: 2
    BACKGROUND_CHECK: 3
    IDENTITY_VERIFICATION_CHECK: 4
