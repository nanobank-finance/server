"""Application Routes."""
import logging
from typing import List, Self, Union

from bizlogic.application import LoanApplicationReader, LoanApplicationWriter

from fastapi import Depends, FastAPI

from ipfsclient.ipfs import Ipfs

from src.schemas import SuccessOrFailureResponse
from src.utils import ParserType, RouterUtils

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class LoanApplicationRouter():
    """Loan Application Router."""

    def __init__(self: Self, app: FastAPI) -> None:
        """Add routes for loan application.

        Args:
            app (FastAPI): Routes will be added to this app.
        """
        ipfsclient = Ipfs()
        loan_application_reader = LoanApplicationReader(ipfsclient)

        # Loan application endpoints

        @app.post("/loan/application", response_model=SuccessOrFailureResponse)
        async def submit_loan_application(
            asking: int,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> SuccessOrFailureResponse:
            """Create a loan application.

            Args:
                asking (int): The amount requested by the borrower.

            Returns:
                SuccessOrFailureResponse: `success=True` when successful.
            """
            borrower = "123"  # TODO: get from KYC
            try:
                loan_application_writer = LoanApplicationWriter(
                    ipfsclient,
                    borrower,
                    asking
                )
                loan_application_writer.write()
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

        @app.get(
            "/loan/application",
            response_model=List
        )
        async def get_all_loan_applications(
            recent: bool = False,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> List:
            """Get all loan applications.

            Args:
                recent (bool, optional): Use CDC or only get the most recent.
                    Defaults to False.

            Returns:
                List: _description_
            """
            results = loan_application_reader.get_open_loan_applications()
            return RouterUtils.parse_results(
                results,
                recent,
                ParserType.LOAN_APPLICATION
            )

        @app.get(
            "/loan/application/user/self",
            response_model=List
        )
        async def get_my_loan_applications(
            recent: bool = False,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> List:
            """Get my loan applications.

            Args:
                recent (bool, optional): Use CDC or only get the most recent.
                    Defaults to False.

            Returns:
                List: _description_
            """
            borrower = "123"  # TODO: get from KYC
            results = loan_application_reader.get_loan_applications_for_borrower(borrower)  # noqa: E501
            return RouterUtils.parse_results(
                results,
                recent,
                ParserType.LOAN_APPLICATION
            )

        @app.get(
            "/loan/application/user/other",
            response_model=List
        )
        async def get_their_loan_applications(
            them: str,
            recent: bool = False,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> List:
            """Get their loan applications.

            Args:
                them (str): The user whose applications to get.
                recent (bool, optional): Use CDC or only get the most recent.
                    Defaults to False.

            Returns:
                List: _description_
            """
            results = loan_application_reader.get_loan_applications_for_borrower(them)  # noqa: E501
            return RouterUtils.parse_results(
                results,
                recent,
                ParserType.LOAN_APPLICATION
            )

        @app.delete(
            "/loan/application/{application}",
            response_model=SuccessOrFailureResponse
        )
        async def withdraw_loan_application(
            application: str,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> SuccessOrFailureResponse:
            """Withdraw a loan application.

            Args:
                application (str): The application to withdraw.

            Returns:
                SuccessOrFailureResponse: `success=True` when successful.
            """
            borrower = "123"  # TODO: get from KYC

            try:
                # query to get the application data
                results = loan_application_reader.get_loan_application(application)  # noqa: E501

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
