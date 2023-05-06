"""Loan Routes."""
import logging
from typing import Any, List, Self, Union

from bizlogic.loan.reader import LoanReader
from bizlogic.loan.repayment import PaymentSchedule
from bizlogic.loan.status import LoanStatusType
from bizlogic.loan.writer import LoanWriter

from fastapi import Depends, FastAPI

from ipfsclient.ipfs import Ipfs

import pandas as pd

from src.schemas import SuccessOrFailureResponse
from src.utils import ParserType, get_user_token
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

        # Loan endpoints

        @app.get(
            "/loans/open",
            response_model=Union[List, SuccessOrFailureResponse]
        )
        async def get_open_loans(
            recent: bool = False,
            user: Any = Depends(get_user_token)
        ) -> Union[List, SuccessOrFailureResponse]:
            try:
                results = loan_reader.query_for_status(
                    LoanStatusType.PENDING_ACCEPTANCE
                )
                return RouterUtils.parse_results(
                    results,
                    recent,
                    ParserType.LOAN
                )
            except Exception as e:
                LOG.exception(e)
                return SuccessOrFailureResponse(
                    success=False,
                    error_message=str(e),
                    error_type=type(e).__name__
                )

        @app.get(
            "/loans/accepted",
            response_model=Union[List, SuccessOrFailureResponse]
        )
        async def get_accepted_loans(
            recent: bool = False,
            user: Any = Depends(get_user_token)
        ) -> Union[List, SuccessOrFailureResponse]:
            try:
                results = loan_reader.query_for_status(LoanStatusType.ACCEPTED)
                return RouterUtils.parse_results(
                    results,
                    recent,
                    ParserType.LOAN
                )
            except Exception as e:
                LOG.exception(e)
                return SuccessOrFailureResponse(
                    success=False,
                    error_message=str(e),
                    error_type=type(e).__name__
                )

        @app.get(
            "/loans/user/self/open",
            response_model=Union[List, SuccessOrFailureResponse]
        )
        async def get_my_open_loans(
            perspective: str = "borrower",
            recent: bool = False,
            user: Any = Depends(get_user_token)
        ) -> Union[List, SuccessOrFailureResponse]:
            assert perspective in ["lender", "borrower"]  # TODO: handle invalid request properly (and make enum instead of str?)  # noqa: E501
            borrower = "123"  # TODO: get from KYC
            try:
                results = loan_reader.query_for_status(
                    LoanStatusType.PENDING_ACCEPTANCE,
                    index={
                        perspective: borrower
                    }
                )
                return RouterUtils.parse_results(
                    results,
                    recent,
                    ParserType.LOAN
                )
            except Exception as e:
                LOG.exception(e)
                return SuccessOrFailureResponse(
                    success=False,
                    error_message=str(e),
                    error_type=type(e).__name__
                )

        @app.get(
            "/loans/user/self/accepted",
            response_model=Union[List, SuccessOrFailureResponse]
        )
        async def get_my_accepted_loans(
            perspective: str = "borrower",
            recent: bool = False,
            user: Any = Depends(get_user_token)
        ) -> Union[List, SuccessOrFailureResponse]:
            assert perspective in ["lender", "borrower"]  # TODO: handle invalid request properly (and make enum instead of str?)  # noqa: E501
            borrower = "123"  # TODO: get from KYC
            try:
                results = loan_reader.query_for_status(
                    LoanStatusType.ACCEPTED,
                    index={
                        perspective: borrower
                    }
                )
                return RouterUtils.parse_results(
                    results,
                    recent,
                    ParserType.LOAN
                )
            except Exception as e:
                LOG.exception(e)
                return SuccessOrFailureResponse(
                    success=False,
                    error_message=str(e),
                    error_type=type(e).__name__
                )

        @app.get(
            "/loans/user/self",
            response_model=Union[List, SuccessOrFailureResponse]
        )
        async def get_my_loans(
            perspective: str = "borrower",
            recent: bool = False,
            user: Any = Depends(get_user_token)
        ) -> Union[List, SuccessOrFailureResponse]:
            assert perspective in ["lender", "borrower"]  # TODO: handle invalid request properly (and make enum instead of str?)  # noqa: E501
            borrower = "123"  # TODO: get from KYC
            try:
                if perspective == "borrower":
                    results = loan_reader.query_for_borrower(borrower)
                elif perspective == "lender":
                    results = loan_reader.query_for_lender(borrower)

                return RouterUtils.parse_results(
                    results,
                    recent,
                    ParserType.LOAN
                )
            except Exception as e:
                LOG.exception(e)
                return SuccessOrFailureResponse(
                    success=False,
                    error_message=str(e),
                    error_type=type(e).__name__
                )

        @app.get(
            "/loans/user/other",
            response_model=Union[List, SuccessOrFailureResponse]
        )
        async def get_their_loans(
            them: str,
            perspective: str = "borrower",
            recent: bool = False,
            user: Any = Depends(get_user_token)
        ) -> Union[List, SuccessOrFailureResponse]:
            assert perspective in ["lender", "borrower"]  # TODO: handle invalid request properly (and make enum instead of str?)  # noqa: E501
            try:
                if perspective == "borrower":
                    results = loan_reader.query_for_borrower(them)
                elif perspective == "lender":
                    results = loan_reader.query_for_lender(them)

                return RouterUtils.parse_results(
                    results,
                    recent,
                    ParserType.LOAN
                )
            except Exception as e:
                LOG.exception(e)
                return SuccessOrFailureResponse(
                    success=False,
                    error_message=str(e),
                    error_type=type(e).__name__
                )

        @app.get(
            "/loan",
            response_model=Union[List, SuccessOrFailureResponse]
        )
        async def get_loan_details(
            loan_id: str,
            recent: bool = False,
            user: Any = Depends(get_user_token)
        ) -> Union[List, SuccessOrFailureResponse]:
            try:
                results = loan_reader.query_for_loan(loan_id)
                return RouterUtils.parse_results(
                    results,
                    recent,
                    ParserType.LOAN
                )
            except Exception as e:
                LOG.exception(e)
                return SuccessOrFailureResponse(
                    success=False,
                    error_message=str(e),
                    error_type=type(e).__name__
                )

        @app.post("/loan", response_model=SuccessOrFailureResponse)
        async def create_loan_offer(
                borrower: str,
                principal: int,
                interest: float,
                duration: int,
                payments: int,
                expiry: int,
                user: Any = Depends(get_user_token)
        ) -> SuccessOrFailureResponse:
            lender = "123"  # TODO: get from KYC
            try:

                offer_expiry_date = RouterUtils.nanosecond_epoch_to_datetime(expiry)  # noqa: E501

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

        # TODO: accept loan offer

        # TODO: make payment
