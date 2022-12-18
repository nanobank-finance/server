from typing import Union
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, asdict
from random import random

class LoanApplicationState(Enum):
    DRAFT = 1
    WITHDRAWN = 2
    COLLECTING_STAKE = 3
    FULLY_FUNDED = 4
    IN_PROGRESS = 5
    DEFAULT = 6
    COMPLETE = 7

class WalletType(Enum):
    WITHDRAW_ONLY = 1  # yield wallets
    DEPOSIT_ONLY = 2  # bill pay wallets
    WITHDRAW_OR_DEPOSIT = 3  # personal wallets
    INTERNAL_ONLY = 4

class LoanPaymentState(Enum):
    SCHEDULED = 1
    UPCOMING = 2
    COMPLETED_ON_TIME = 3
    LATE = 4
    COMPLETED_LATE = 5
    MISSED = 6

@dataclass
class User:
    uid: str

@dataclass
class WalletStatus:
    is_frozen: bool
    frozen_reason_code: int
    doc_id: str = random()
    reasons = {
        101: "missing_user_verification",
        102: "fraud_suspected",
        103: "staked_for_loan"
    }
 
@dataclass
class LoanPaymentStatus:
    state: LoanPaymentState
    next: Union[object, None]
    previous: Union[object, None]
    timestamp: datetime
    doc_id: str = random()

@dataclass   
class LoanApplicationStatus:
    state: LoanApplicationState
    next: Union[object, None]
    previous: Union[object, None]
    timestamp: datetime
    doc_id: str = random()

@dataclass   
class Wallet:
    owner: Union[User, None]
    wallet_type: Union[WalletType, int, None]
    address: Union[float, str]
    key: Union[str, None]
    status: Union[WalletStatus, object, None]
    doc_id: float = random()

@dataclass
class Loan:
    def __init__(
            self,
            principal_in_xno,
            loan_start_date,
            monthly_payment,
            monthly_interest_rate,
            number_of_payment_periods,
            status,
            payment_wallet,
            principal_wallet,
            borrower):
        self.doc_id: str = random()
        self.principal_in_xno: float = principal_in_xno
        self.loan_start_date: datetime = loan_start_date
        self.monthly_payment: float = monthly_payment
        self.monthly_interest_rate: float = monthly_interest_rate
        self.number_of_payment_periods: int = number_of_payment_periods
        self.status: LoanApplicationStatus = status
        self.payment_wallet: Wallet = payment_wallet
        self.principal_wallet: Wallet = principal_wallet
        self.borrower: User = borrower
        
    def to_dict(self):
        return {
            "doc_id": self.doc_id,
            "principal_in_xno": self.principal_in_xno,
            "loan_start_date": self.loan_start_date,
            "monthly_payment": self.monthly_payment,
            "monthly_interest_rate": self.monthly_interest_rate,
            "number_of_payment_periods": self.number_of_payment_periods,
            "status": self.status,
            "payment_wallet": self.payment_wallet,
            "principal_wallet": self.principal_wallet,
            "borrower": self.borrower
        }

@dataclass
class Stake:
    def __init__(
            self,
            owner,
            stake_start_date,
            stake_from_wallet,
            yield_wallet,
            monthly_interest_rate,
            monthly_payment,
            number_of_payment_periods):
        self.doc_id: str = random()
        self.owner: User = owner
        self.start_date: datetime = stake_start_date
        self.from_wallet: Wallet = stake_from_wallet
        self.yield_wallet: Wallet = yield_wallet
        self.monthly_interest_rate: float = monthly_interest_rate
        self.monthly_payment: float = monthly_payment
        self.number_of_payment_periods: float = number_of_payment_periods
        
    def to_dict(self):
        return {
            "doc_id": self.doc_id,
            "owner": self.owner,
            "start_date": self.start_date,
            "from_wallet": self.from_wallet,
            "yield_wallet": self.yield_wallet,
            "monthly_interest_rate": self.monthly_interest_rate,
            "monthly_payment": self.monthly_payment,
            "number_of_payment_periods": self.number_of_payment_periods
        }

@dataclass
class LoanPayment:
    def __init__(self, loan, due_date, amount_due_in_xno, status):
        self.doc_id: str = random()
        self.loan: Loan = loan
        self.due_date: datetime = due_date
        self.amount_due_in_xno: float = amount_due_in_xno
        self.status: LoanPaymentStatus = status
        
    def to_dict(self):
        return {
            "doc_id": self.doc_id,
            "loan": self.loan,
            "due_date": self.due_date,
            "amount_due_in_xno": self.amount_due_in_xno,
            "status": self.status
        }
