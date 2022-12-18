from __future__ import annotations
from typing import Union
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, asdict
from random import random

""" Enums """

class WalletType(Enum):
    WITHDRAW_ONLY = 1  # yield wallets
    DEPOSIT_ONLY = 2  # bill pay wallets
    WITHDRAW_OR_DEPOSIT = 3  # personal wallets
    INTERNAL_ONLY = 4

class WalletState(Enum):
    FROZEN_MISSING_USER_VERIFICATION: 1
    FROZEN_FRAUD_SUSPECTED = 2
    FROZEN_STAKED_FOR_LOAN = 3
    VALID_ACTIVE_WALLET = 4

class LoanApplicationState(Enum):
    DRAFT = 1
    WITHDRAWN = 2
    COLLECTING_STAKE = 3
    FULLY_FUNDED = 4
    IN_PROGRESS = 5
    DEFAULT = 6
    COMPLETE = 7

class LoanPaymentState(Enum):
    SCHEDULED = 1
    UPCOMING = 2
    COMPLETED_ON_TIME = 3
    LATE = 4
    COMPLETED_LATE = 5
    MISSED = 6

""" Object Status Classes (for tracking entity workflows) """

@dataclass
class WalletStatus:
    state: WalletState
    is_frozen: bool
    next: Union[WalletStatus, None]
    previous: Union[WalletStatus, None]
    timestamp: datetime
    doc_id: str = random()
 
@dataclass
class LoanPaymentStatus:
    state: LoanPaymentState
    next: Union[LoanPaymentStatus, None]
    previous: Union[LoanPaymentStatus, None]
    timestamp: datetime
    doc_id: str = random()

@dataclass   
class LoanApplicationStatus:
    state: LoanApplicationState
    next: Union[LoanApplicationStatus, None]
    previous: Union[LoanApplicationStatus, None]
    timestamp: datetime
    doc_id: str = random()

""" Entities """

@dataclass
class User:
    uid: str

@dataclass   
class Wallet:
    owner: Union[User, None]
    wallet_type: WalletType
    address: Union[float, str]
    key: Union[str, None]
    status: WalletStatus
    doc_id: float = random()

@dataclass
class Loan:
    principal_in_xno: float
    loan_start_date: datetime
    monthly_payment: float
    monthly_interest_rate: float
    number_of_payment_periods: int
    status: LoanApplicationStatus
    payment_wallet: Wallet
    principal_wallet: Wallet
    borrower: User
    doc_id: float = random()
    
@dataclass
class Stake:
    owner: User
    start_date: datetime
    from_wallet: Wallet
    yield_wallet: Wallet
    monthly_interest_rate: float
    monthly_payment: float
    number_of_payment_periods: float
    doc_id: float = random()

@dataclass
class LoanPayment:
    loan: Loan
    due_date: datetime
    amount_due_in_xno: float
    status: LoanPaymentStatus
    doc_id: float = random()
