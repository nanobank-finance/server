from fastapi import Depends
from typing import List
from src.schemas import SuccessOrFailResponse
from src.utils import get_user_token
from ipfsclient.ipfs import Ipfs
from bizlogic.loan.reader import LoanReader
from bizlogic.application.reader import LoanApplicationReader

class LoanRouter():

    def __init__(self, app):

        ipfsclient = Ipfs()
        loan_reader = LoanReader(ipfsclient)
        loan_application_reader = LoanApplicationReader(ipfsclient)

        # Loan application endpoints

        @app.post("/loan/application", response_model=SuccessOrFailResponse)
        async def submit_loan_application(user = Depends(get_user_token)):
            return {"Hello": "World"}

        @app.delete("/loan/application/{loan_id}", response_model=SuccessOrFailResponse)
        async def withdraw_loan_application(loan_id: int, user = Depends(get_user_token)):
            return {"Hello": "World"}

        # Loan endpoints

        @app.get("/loans")
        async def get_all_loans(user = Depends(get_user_token)):
            return {"Hello": "World"}

        @app.get("/loans/user")
        async def get_my_loans(user = Depends(get_user_token)):
            return {"Hello": "World"}

        @app.get("/loan/{loan_id}") #response_model=Union[schemas.Loan, SuccessOrFailResponse])
        async def get_loan_details(loan_id: int, user = Depends(get_user_token)):
            return {"Hello": "World"}
