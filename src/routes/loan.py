from fastapi import Depends
import logging
from typing import List
import json
import datetime
from datetime import timezone
import pandas as pd
from src.schemas import SuccessOrFailResponse
from src.utils import get_user_token
from ipfsclient.ipfs import Ipfs
from bizlogic.loan.reader import LoanReader
from bizlogic.loan.writer import LoanWriter
from bizlogic.application import LoanApplicationReader, LoanApplicationWriter


LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class LoanRouter():

    def __init__(self, app):

        ipfsclient = Ipfs()
        loan_reader = LoanReader(ipfsclient)

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
