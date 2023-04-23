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


LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class LoanRouter():


    def nanosecond_epoch_to_datetime(self, timestamp):
        timestamp = int(timestamp)
        seconds = timestamp // 1000000000
        nanoseconds = timestamp % 1000000000
        return datetime.datetime.fromtimestamp(seconds) + datetime.timedelta(microseconds=nanoseconds // 1000)

    def get_most_recent(self, df, group_by):
        # Get the most recent data for each application

        # convert the "created" field to datetime format
        df['created'] = self.nanosecond_epoch_to_datetime(df['created'])

        # group by "application" and get the row with the maximum "created" timestamp per group
        max_created_per_app = df.groupby(group_by)['created'].max().reset_index()

        # join the original dataframe with the grouped data to get the full row with the maximum "created" per application
        return pd.merge(df, max_created_per_app, on=[group_by, 'created'], how='inner')


    def __init__(self, app):

        ipfsclient = Ipfs()
        loan_reader = LoanReader(ipfsclient)
        loan_application_reader = LoanApplicationReader(ipfsclient)

        # Loan application endpoints

        @app.post("/loan/application", response_model=SuccessOrFailResponse)
        async def submit_loan_application(asking: int): #, user = Depends(get_user_token)):
            borrower = "123"  # TODO: get from KYC
            try:
                loan_application_writer = LoanApplicationWriter(ipfsclient, borrower, asking)
                loan_application_writer.write()
            except Exception as e:
                return SuccessOrFailResponse(
                    success=False,
                    error_message=str(e)
                )

            return SuccessOrFailResponse(
                success=True
            )
        
        @app.get("/loan/application")
        async def get_borrower_loan_applications(user = Depends(get_user_token), recent: bool = False):
            borrower = "123"  # TODO: get from KYC
            try:
                results = loan_application_reader.get_loan_applications_for_borrower(borrower)
            except Exception as e:
                return SuccessOrFailResponse(
                    success=False,
                    error_message=e
                )

            df = Store.to_dataframe(results, protobuf_parsers={
                "amount_asking": lambda store: store.reader.amount_asking,
                "closed": lambda store: store.reader.closed,
            })
            LOG.debug(df)
            if len(df) == 0:
                return []

            df.created = pd.to_numeric(df.created)
            if recent:
                df = self.get_most_recent(df, "application")

            return json.loads(df.to_json(orient="records"))

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
            except Exception as e:
                return SuccessOrFailResponse(
                    success=False,
                    error_message=str(e)
                )

            return SuccessOrFailResponse(
                success=True
            )

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
