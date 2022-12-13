from typing import Union, TypeVar, Generic
from pydantic import BaseModel
from enum import Enum

T = TypeVar('T')

""" api request/response models """

class CheckType(Enum):
    CREDIT_CHECK: 1
    PROOF_OF_INCOME_CHECK: 2
    BACKGROUND_CHECK: 3
    IDENTITY_VERIFICATION_CHECK: 4

class SuccessOrFailResponse(BaseModel):
    success: bool
    error_message: Union[str, None] = None
    error_code: Union[int, None] = None

class WalletModel(BaseModel):
    name: str

class SavingsInterestModel(BaseModel):
    name: str

class LoanApplicationModel(BaseModel):
    name: str

class TokenResponse(BaseModel):
    token: str

""" database models """

class Wallet(object):
    def __init__(self):
        pass

class SavingsInterest(object):
    def __init__(self):
        pass

class LoanApplication(object):
    def __init__(self, name, state, country, capital=False, population=0,
                 regions=[]):
        self.name = name
        self.state = state
        self.country = country
        self.capital = capital
        self.population = population
        self.regions = regions

    @staticmethod
    def from_dict(source):
        # ...
        pass

    def to_dict(self):
        # ...
        pass

    def __repr__(self):
        return (
            f'City(\
                name={self.name}, \
                country={self.country}, \
                population={self.population}, \
                capital={self.capital}, \
                regions={self.regions}\
            )'
        )
