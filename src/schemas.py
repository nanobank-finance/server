from typing import Union
from pydantic import BaseModel
from enum import Enum

class CheckType(Enum):
    CREDIT_CHECK: 1
    PROOF_OF_INCOME_CHECK: 2
    BACKGROUND_CHECK: 3
    IDENTITY_VERIFICATION_CHECK: 4

class SuccessOrFailResponse(BaseModel):
    success: bool
    error_message: Union[str, None] = None

class Wallet(object):
    def __init__(self):
        pass

class SavingsInterest(object):
    def __init__(self):
        pass

class LoanApplication(object):
    def __init__(self, name, state, country, capital=False, population=0, regions=[]):
        self.name = name
        self.state = state
        self.country = country
        self.capital = capital
        self.population = population
        self.regions = regions

    @staticmethod
    def from_dict(source):
        pass

    def to_dict(self):
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
