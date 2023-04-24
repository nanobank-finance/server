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
from bizlogic.loan.status import LoanStatusType
from bizlogic.loan.reader import LoanReader
from bizlogic.loan.writer import LoanWriter
from bizlogic.loan.repayment import PaymentSchedule
from src.utils import RouterUtils


LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class LoanRouter():

    def __init__(self, app):

        ipfsclient = Ipfs()
        loan_reader = LoanReader(ipfsclient)

        # Loan endpoints

        @app.get("/loans/open")
        async def get_open_loans(recent: bool = False, user = Depends(get_user_token)):
            try:
                results = loan_reader.query_for_status(LoanStatusType.PENDING_ACCEPTANCE)
                return RouterUtils.parse_results(results, recent)
            except Exception as e:
                return SuccessOrFailResponse(
                    success=False,
                    error_message=str(e)
                )

        @app.get("/loans/accepted")
        async def get_accepted_loans(recent: bool = False, user = Depends(get_user_token)):
            try:
                results = loan_reader.query_for_status(LoanStatusType.ACCEPTED)
                return RouterUtils.parse_results(results, recent)
            except Exception as e:
                return SuccessOrFailResponse(
                    success=False,
                    error_message=str(e)
                )

        @app.get("/loans/user")
        async def get_my_loans(user = Depends(get_user_token)):
            return {"Hello": "World"}

        @app.get("/loan/{loan_id}") #response_model=Union[schemas.Loan, SuccessOrFailResponse])
        async def get_loan_details(loan_id: int, user = Depends(get_user_token)):
            return {"Hello": "World"}

        @app.post("/loan") #response_model=Union[schemas.Loan, SuccessOrFailResponse])
        async def create_loan_offer(
                borrower: str,
                principal: int,
                interest: float,
                duration: int,
                payments: int,
                expiry: int,
                user = Depends(get_user_token)):
            lender = "123"  # TODO: get from KYC
            try:

                offer_expiry_date = RouterUtils.nanosecond_epoch_to_datetime(expiry)

                payment_schedule = PaymentSchedule.create_payment_schedule(
                    amount=principal,
                    interest_rate=interest,
                    total_duration=pd.Timedelta(duration, unit='ns'),
                    number_of_payments=payments,
                    first_payment=offer_expiry_date
                )

                loan_writer = LoanWriter(
                    ipfsclient,
                    borrower,
                    lender,
                    principal,
                    payment_schedule,
                    offer_expiry=offer_expiry_date
                )

                loan_writer.write()

                return SuccessOrFailResponse(
                    success=True
                )
            except Exception as e:
                return SuccessOrFailResponse(
                    success=False,
                    error_message=str(e)
                )
