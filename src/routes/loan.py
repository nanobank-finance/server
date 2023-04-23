from fastapi import Depends
from typing import List
import json
import pandas as pd
from src.schemas import SuccessOrFailResponse
from src.utils import get_user_token
from ipfsclient.ipfs import Ipfs
from ipfskvs.store import Store
from bizlogic.loan.reader import LoanReader
from bizlogic.loan.writer import LoanWriter
from bizlogic.application import LoanApplicationReader, LoanApplicationWriter

class LoanRouter():

    def __init__(self, app):

        ipfsclient = Ipfs()
        loan_reader = LoanReader(ipfsclient)
        loan_application_reader = LoanApplicationReader(ipfsclient)
        # loan_writer = LoanWriter(ipfsclient)


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
                    error_message=e
                )

            return SuccessOrFailResponse(
                success=True
            )
        
        @app.get("/loan/application")
        async def get_borrower_loan_applications(user = Depends(get_user_token), most_recent: bool = False):
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
            df.created = pd.to_numeric(df.created)
            df.index = df.created

            if most_recent:
                # TODO: group by 'created' on 'application'
                # Get the most recent data for each application
                # df = df.loc[df['created'].idxmax()]
                pass

            return json.loads(df.to_json(orient="index"))

        @app.delete("/loan/application/{loan_id}", response_model=SuccessOrFailResponse)
        async def withdraw_loan_application(loan_id: int, user = Depends(get_user_token)):
            borrower = "123"  # TODO: get from KYC
            try:
                # get loan for id
                results = loan_application_reader.get_loan_applications_for_borrower(borrower)
                print(results)

                # # make the update and write it to IPFS
                # loan_application_writer = LoanApplicationWriter(ipfsclient, borrower, asking)
                # loan_application_writer.
                # loan_application_writer.write()
            except Exception as e:
                return SuccessOrFailResponse(
                    success=False,
                    error_message=e
                )

            return results

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
