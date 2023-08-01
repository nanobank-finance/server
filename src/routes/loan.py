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
            "/loans/open",
            response_model=dict
        )
        async def get_open_loans(
            recent: bool = False,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> List:
            """Get all open loans.

            Args:
                recent (bool, optional): If True, only return the most recent
                    loan. Defaults to False.
                user (str, optional): User token. Defaults to Depends(RouterUtils.get_user_token).

            Returns:
                List: List of loans.
            """
            return loan_reader.query_for_status(
                LoanStatusType.PENDING_ACCEPTANCE,
                recent_only=recent
            ).to_dict(orient="records")

        @app.get(
            "/loans/accepted",
            response_model=dict
        )
        async def get_accepted_loans(
            recent: bool = False,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> List:
            """Get all accepted loans.

            Args:
                recent (bool, optional): If True, only return the most recent
                    loan. Defaults to False.
                user (str, optional): User token. Defaults to Depends(RouterUtils.get_user_token).

            Returns:
                List: List of loans.
            """
            return loan_reader.query_for_status(
                LoanStatusType.ACCEPTED,
                recent_only=recent
            ).to_dict(orient="records")

        @app.get(
            "/loans/user/self/open",
            response_model=List[LoanResponse]
        )
        async def get_my_open_loans(
            perspective: str = "borrower",
            recent: bool = False,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> List[LoanResponse]:
            """Get all open loans for the user.

            Args:
                perspective (str, optional): The perspective of the user.
                    Defaults to "borrower".
                recent (bool, optional): If True, only return the most recent
                    loan. Defaults to False.
                user (str, optional): User token. Defaults to Depends(RouterUtils.get_user_token).

            Returns:
                List: List of loans.
            """
            assert perspective in ["lender", "borrower"]  # TODO: handle invalid request properly (and make enum instead of str?)  # noqa: E501

            results = loan_reader.query_for_status(
                LoanStatusType.PENDING_ACCEPTANCE,
                index={
                    perspective: user
                }
            )

            LOG.debug("Results: %s", results)

            return RouterUtils.sanitize_output(results.to_dict(orient="records"))

        @app.get(
            "/loans/user/self/draft",
            response_model=List[LoanResponse]
        )
        async def get_my_draft_loan_offers(
            perspective: str = "lender",
            recent: bool = False,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> List[LoanResponse]:
            """Get all open loans for the user.

            Args:
                perspective (str, optional): The perspective of the user.
                    Defaults to "borrower".
                recent (bool, optional): If True, only return the most recent
                    loan. Defaults to False.
                user (str, optional): User token. Defaults to Depends(RouterUtils.get_user_token).

            Returns:
                List: List of loans.
            """
            assert perspective in ["lender", "borrower"]  # TODO: handle invalid request properly (and make enum instead of str?)  # noqa: E501

            results = loan_reader.query_for_status(
                LoanStatusType.DRAFT,
                index={
                    perspective: user
                }
            )

            LOG.debug("Results: %s", results)

            return RouterUtils.sanitize_output(results.to_dict(orient="records"))

        @app.get(
            "/loans/user/their/open",
            response_model=dict
        )
        async def get_their_open_loans(
            them: int,
            perspective: str = "borrower",
            recent: bool = False,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> List:
            """Get all open loans for the user.

            Args:
                them (int): The user ID of the user.
                perspective (str, optional): The perspective of the user.
                    Defaults to "borrower".
                recent (bool, optional): If True, only return the most recent
                    loan. Defaults to False.
                user (str, optional): User token. Defaults to Depends(RouterUtils.get_user_token).

            Returns:
                List: List of loans.
            """
            assert perspective in ["lender", "borrower"]
            results = loan_reader.query_for_status(
                LoanStatusType.PENDING_ACCEPTANCE,
                index={
                    perspective: them
                },
                recent_only=recent
            )
            return results.to_dict(orient="records")

        @app.get(
            "/loans/user/self/accepted",
            response_model=dict
        )
        async def get_my_accepted_loans(
            perspective: str = "borrower",
            recent: bool = False,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> List:
            """Get all accepted loans for the user.

            Args:
                perspective (str, optional): The perspective of the user.
                    Defaults to "borrower".
                recent (bool, optional): If True, only return the most recent
                    loan. Defaults to False.
                user (str, optional): User token. Defaults to Depends(RouterUtils.get_user_token).

            Returns:
                List: List of loans.
            """
            assert perspective in ["lender", "borrower"]  # TODO: handle invalid request properly (and make enum instead of str?)  # noqa: E501
            borrower = "123"  # TODO: get from KYC
            results = loan_reader.query_for_status(
                LoanStatusType.ACCEPTED,
                index={
                    perspective: borrower
                },
                recent_only=recent
            )
            return results.to_dict(orient="records")

        @app.get(
            "/loans/user/their/accepted",
            response_model=dict
        )
        async def get_their_accepted_loans(
            them: int,
            perspective: str = "borrower",
            recent: bool = False,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> List:
            """Get all accepted loans for the user.

            Args:
                them (int): The user ID of the user.
                perspective (str, optional): The perspective of the user.
                    Defaults to "borrower".
                recent (bool, optional): If True, only return the most recent
                    loan. Defaults to False.
                user (str, optional): User token. Defaults to Depends(RouterUtils.get_user_token).

            Returns:
                List: List of loans.
            """
            assert perspective in ["lender", "borrower"]
            results = loan_reader.query_for_status(
                LoanStatusType.ACCEPTED,
                index={
                    perspective: them
                },
                recent_only=recent
            )

            return results.to_dict(orient="records")

        @app.get(
            "/loans/user/self",
            response_model=dict
        )
        async def get_my_loans(
            perspective: str = "borrower",
            recent: bool = False,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> List:
            """Get all loans for the user.

            Args:
                perspective (str, optional): The perspective of the user.
                    Defaults to "borrower".
                recent (bool, optional): If True, only return the most recent
                    loan. Defaults to False.
                user (str, optional): User token. Defaults to Depends(RouterUtils.get_user_token).

            Returns:
                List: List of loans.
            """
            assert perspective in ["lender", "borrower"]  # TODO: handle invalid request properly (and make enum instead of str?)  # noqa: E501
            borrower = "123"  # TODO: get from KYC
            if perspective == "borrower":
                results = loan_reader.query_for_borrower(borrower, recent_only=recent)
            elif perspective == "lender":
                results = loan_reader.query_for_lender(borrower, recent_only=recent)

            return results.to_dict(orient="records")

        @app.get(
            "/loans/user/other",
            response_model=dict
        )
        async def get_their_loans(
            them: str,
            perspective: str = "borrower",
            recent: bool = False,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> List:
            """Get all loans for the user.

            Args:
                them (str): The user ID of the user.
                perspective (str, optional): The perspective of the user.
                    Defaults to "borrower".
                recent (bool, optional): If True, only return the most recent
                    loan. Defaults to False.
                user (str, optional): User token. Defaults to Depends(RouterUtils.get_user_token).

            Returns:
                List: List of loans.
            """
            assert perspective in ["lender", "borrower"]  # TODO: handle invalid request properly (and make enum instead of str?)  # noqa: E501
            if perspective == "borrower":
                results = loan_reader.query_for_borrower(them)
            elif perspective == "lender":
                results = loan_reader.query_for_lender(them)

            return results.to_dict(orient="records")

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


        # TODO: make payment
