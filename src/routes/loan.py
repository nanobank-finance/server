"""Loan Routes."""
import logging
from typing import List, Self, Union

from bizlogic.loan.reader import LoanReader
from bizlogic.loan.repayment import PaymentSchedule
from bizlogic.loan.status import LoanStatusType
from bizlogic.loan.writer import LoanWriter
from bizlogic.utils import ParserType, Utils

from fastapi import Depends, FastAPI

from ipfsclient.ipfs import Ipfs

import pandas as pd

from src.schemas import SuccessOrFailureResponse
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

        @app.get(
            "/loans/open",
            response_model=List
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
            results = loan_reader.query_for_status(
                LoanStatusType.PENDING_ACCEPTANCE
            )
            return Utils.parse_results(
                results,
                recent,
                ParserType.LOAN
            )

        @app.get(
            "/loans/accepted",
            response_model=List
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
            results = loan_reader.query_for_status(LoanStatusType.ACCEPTED)
            return Utils.parse_results(
                results,
                recent,
                ParserType.LOAN
            )

        @app.get(
            "/loans/user/self/open",
            response_model=List
        )
        async def get_my_open_loans(
            perspective: str = "borrower",
            recent: bool = False,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> List:
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
            borrower = "123"  # TODO: get from KYC
            results = loan_reader.query_for_status(
                LoanStatusType.PENDING_ACCEPTANCE,
                index={
                    perspective: borrower
                }
            )
            return Utils.parse_results(
                results,
                recent,
                ParserType.LOAN
            )

        @app.get(
            "/loans/user/their/open",
            response_model=List
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
                }
            )
            return Utils.parse_results(
                results,
                recent,
                ParserType.LOAN
            )

        @app.get(
            "/loans/user/self/accepted",
            response_model=List
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
                }
            )
            return Utils.parse_results(
                results,
                recent,
                ParserType.LOAN
            )
        
        @app.get(
            "/loans/user/their/accepted",
            response_model=List
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
                }
            )

            return results.to_json(orient="records")

        @app.get(
            "/loans/user/self",
            response_model=List
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
                results = loan_reader.query_for_borrower(borrower)
            elif perspective == "lender":
                results = loan_reader.query_for_lender(borrower)

            return results.to_json(orient="records")

        @app.get(
            "/loans/user/other",
            response_model=List
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

            return results.to_json(orient="records")

        @app.get(
            "/loan",
            response_model=List
        )
        async def get_loan_details(
            loan_id: str,
            recent: bool = False,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> List:
            """Get all loans for the user.

            Args:
                loan_id (str): The loan ID of the loan.
                recent (bool, optional): If True, only return the most recent
                    loan. Defaults to False.

            Returns:
                List: List of loans.
            """
            return loan_reader.query_for_loan(loan_id).to_json(orient="records")

        @app.post("/loan", response_model=SuccessOrFailureResponse)
        async def create_loan_offer(
                borrower: str,
                principal: int,
                interest: float,
                duration: int,
                payments: int,
                expiry: int,
                user: str = Depends(RouterUtils.get_user_token)
        ) -> SuccessOrFailureResponse:
            """Create a loan offer.

            Args:
                borrower (str): The borrower ID.
                principal (int): The principal amount.
                interest (float): The interest rate.
                duration (int): The duration of the loan.
                payments (int): The number of payments.
                expiry (int): The expiry of the loan.
            
            Returns:
                SuccessOrFailureResponse: The response.
            """
            lender = "123"  # TODO: get from KYC
            try:

                offer_expiry_date = Utils.nanosecond_epoch_to_datetime(expiry)  # noqa: E501

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
