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
from ipfskvs.store import Store
from bizlogic.loan.reader import LoanReader
from bizlogic.loan.writer import LoanWriter
from bizlogic.application import LoanApplicationReader, LoanApplicationWriter
from src.utils import RouterUtils


LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class LoanApplicationRouter():

    def __init__(self, app):

        ipfsclient = Ipfs()
        loan_application_reader = LoanApplicationReader(ipfsclient)

        # Loan application endpoints

        @app.post("/loan/application", response_model=SuccessOrFailResponse)
        async def submit_loan_application(asking: int, user = Depends(get_user_token)):
            borrower = "123"  # TODO: get from KYC
            try:
                loan_application_writer = LoanApplicationWriter(ipfsclient, borrower, asking)
                loan_application_writer.write()
                return SuccessOrFailResponse(
                    success=True
                )
            except Exception as e:
                return SuccessOrFailResponse(
                    success=False,
                    error_message=str(e)
                )
        
        @app.get("/loan/application")
        async def get_all_loan_applications(recent: bool = False, user = Depends(get_user_token)):
            try:
                results = loan_application_reader.get_open_loan_applications()
                return RouterUtils.parse_results(results, recent)
            except Exception as e:
                return SuccessOrFailResponse(
                    success=False,
                    error_message=e
                )

        @app.get("/loan/user/application")
        async def get_my_loan_applications(recent: bool = False, user = Depends(get_user_token)):
            borrower = "123"  # TODO: get from KYC

            try:
                results = loan_application_reader.get_loan_applications_for_borrower(borrower)
                return RouterUtils.parse_results(results, recent)
            except Exception as e:
                return SuccessOrFailResponse(
                    success=False,
                    error_message=e
                )

        @app.delete("/loan/application/{application}", response_model=SuccessOrFailResponse)
        async def withdraw_loan_application(application: str, user = Depends(get_user_token)):
            borrower = "123"  # TODO: get from KYC

            try:
                # query to get the application data
                results = loan_application_reader.get_loan_application(application)

                # parse the results
                for result in results:
                    loan_application_writer = LoanApplicationWriter(
                        ipfsclient,
                        borrower,
                        result.reader.amount_asking,
                        result.reader.closed
                    )

                    # withdraw the application
                    loan_application_writer.withdraw_loan_application()
                    loan_application_writer.write()

                return SuccessOrFailResponse(
                    success=True
                )
            except Exception as e:
                return SuccessOrFailResponse(
                    success=False,
                    error_message=str(e)
                )
