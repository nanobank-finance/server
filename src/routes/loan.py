"""Loan Routes."""
import datetime
import logging
from typing import List, Self, Union
import os

from bizlogic.loan.reader import LoanReader
from bizlogic.loan.repayment import PaymentSchedule
from bizlogic.loan.status import LoanStatusType, LoanStatus
from bizlogic.loan.writer import LoanWriter
from bizlogic.protoc.loan_pb2 import Loan, LoanPayment
from bizlogic.utils import ParserType, Utils

from fastapi import Depends, FastAPI

from ipfsclient.ipfs import Ipfs

import pandas as pd
from src import uuid_images
from nanohelp.secret import SecretManager

from src.schemas import LoanDetailResponse, LoanOffer, LoanResponse, SuccessOrFailureResponse  # noqa: E501
from src.utils import RouterUtils

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class LoanRouter():
    """Loan Router."""

    def __init__(self: Self, app: FastAPI) -> None:
        """Add routes for loans.

        Args:
            app (FastAPI): Routes will be added to this app.
        """
        ipfsclient = Ipfs()
        loan_reader = LoanReader(ipfsclient)
        secret_manager = SecretManager()

        @app.get(
            "/loans",
            response_model=List[LoanResponse]
        )
        async def get_all_loans(
            recent: bool = False,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> List[LoanResponse]:
            """Get all open loans.

            Args:
                recent (bool, optional): If True, only return the most recent
                    loan. Defaults to False.
                user (str, optional): User token. Defaults to Depends(RouterUtils.get_user_token).

            Returns:
                List: List of loans.
            """
            results = loan_reader.get_all_loans(recent_only=recent)

            LOG.debug("Results: %s", results)
            # results = uuid_images.add_uuid_images(results)
            # results = RouterUtils.sanitize_output(results.to_dict(orient='records'))
            LOG.debug("Final results: %s", results)
            return results if not results.empty else []

        @app.get(
            "/loan",
            response_model=LoanDetailResponse
        )
        async def get_loan_details(
            loan_id: str,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> LoanDetailResponse:
            """Get all loans for the user.

            Args:
                loan_id (str): The loan ID of the loan.
                recent (bool, optional): If True, only return the most recent
                    loan. Defaults to False.

            Returns:
                List: List of loans.
            """
            response = loan_reader.query_for_loan_details(loan_id, recent_only=True)[0]

            # add links to images
            LOG.debug("Before adding image links: %s", response)
            response = uuid_images.add_uuid_images(response)
            LOG.debug("After adding image links: %s", response)

            # add loan status
            LOG.debug("Before adding loan status: %s", response)
            loan = {
                'loan_id': response['metadata']['loan'],
                'borrower': response['metadata']['borrower'],
                'lender': response['metadata']['lender'],
                'principal': int(response['principalAmount']),
                'payments': [
                    {
                        'payment_id': payment['paymentId'],
                        'payment_date': payment['dueDate'],
                        'amount': int(payment['amountDue']),
                    } 
                    for payment in response['repaymentSchedule']
                ],
                'offer_expiry': datetime.datetime.fromisoformat(response['offerExpiry'].replace('Z', '+00:00')),
                'created': response['metadata']['created'],
                'accepted': response.get('accepted', False)
            }

            loan_status = LoanStatus.loan_status(loan)
            LOG.debug("Loan status: %s", loan_status)

            response['metadata']['loan_status'] = loan_status.value

            LOG.debug("After adding loan status: %s", response)
            return response

        @app.post("/loan", response_model=SuccessOrFailureResponse)
        async def create_loan_offer(
            loan: LoanOffer,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> SuccessOrFailureResponse:
            """Create a loan offer."""
            try:
                payment_schedule = PaymentSchedule.create_payment_schedule(
                    principal=loan.principal,
                    interest_rate=loan.interest,
                    start_date=loan.start,
                    end_date=loan.maturity,
                    number_of_payments=loan.payments
                )

                LOG.debug("Project: %s", os.environ.get("GCLOUD_PROJECT_ID"))
                loan_writer = LoanWriter(
                    ipfsclient,
                    loan.borrower,
                    user,
                    int(loan.principal),
                    payment_schedule,
                    offer_expiry=loan.expiry,
                    secret_manager=secret_manager,
                    project=os.environ.get("GCLOUD_PROJECT_ID")
                )

                loan_writer.write()

                return SuccessOrFailureResponse(
                    success=True
                )
            except Exception as e:
                LOG.exception(e)
                return SuccessOrFailureResponse(
                    success=False,
                    error_message=str(e),
                    error_type=type(e).__name__
                )

        @app.post("/loan/accept", response_model=SuccessOrFailureResponse)
        async def accept_loan(
            loan_id: str,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> SuccessOrFailureResponse:
            """Accept a loan.

            Args:
                loan_id (str): The loan ID.

            Returns:
                SuccessOrFailureResponse: The response.
            """
            # read the loan
            results = loan_reader.query_for_loan(loan_id)
            print(results)
