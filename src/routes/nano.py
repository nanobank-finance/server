from http.client import HTTPException
from fastapi import FastAPI, Depends
from src.schemas import NanoAddressResponse
from src.utils import RouterUtils
from src.firestore import db
from src.firestore.crud import check_locked, check_and_lock_user
from nanohelp.wallet import WalletManager
from nanohelp.secret import SecretManager
from bizlogic.loan.reader import LoanReader
from ipfsclient.ipfs import Ipfs

class NanoRouter:
    def __init__(self, app: FastAPI) -> None:
        self.wallet_manager = WalletManager(SecretManager())
        ipfsclient = Ipfs()
        loan_reader = LoanReader(ipfsclient)

        @app.get("/wallet/deposit", response_model=NanoAddressResponse)
        async def get_deposit_address(
            loan_id: str,
            perspective: str,
            user: str = Depends(RouterUtils.get_user_token)) -> NanoAddressResponse:

            # TODO: check if user is valid perspective based on loan data

            loan = loan_reader.query_for_loan_details(loan_id, recent_only=True)[0]
            if perspective == loan.borrower:
                nano_address = loan.borrower_nano_address
            elif perspective == loan.lender:
                nano_address = loan.lender_nano_address
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Perspective must be either borrower or lender"
                )

            return NanoAddressResponse(nano_address=nano_address)

        @app.get("/payments/borrower/completed", response_model=NanoAddressResponse)
        async def get_borrower_payment_history(
                borrower_deposit_address: str,
                user: str = Depends(RouterUtils.get_user_token)) -> NanoAddressResponse:
            """Check if the borrower has made the principal payment.

            Args:
                loan_id (str): _description_
                user (str, optional): _description_. Defaults to Depends(RouterUtils.get_user_token).
            """
            # TODO
            # loan = loan_reader.query_for_loan_details(loan_id, recent_only=True)[0]
            # if user != loan.borrower:
            #     raise HTTPException(
            #         status_code=400,
            #         detail="User must be the borrower"
            #     )

            # nano_address = loan.borrower_nano_address

            # return NanoAddressResponse(nano_address=nano_address)
            pass

        @app.get("/payments/lender/completed", response_model=NanoAddressResponse)
        async def get_lender_payment_history(
                lender_deposit_address: str,
                user: str = Depends(RouterUtils.get_user_token)) -> NanoAddressResponse:
            """Check if the lender has made any repayments.

            Args:
                loan_id (str): _description_
                user (str, optional): _description_. Defaults to Depends(RouterUtils.get_user_token).
            """

            # TODO
            # loan = loan_reader.query_for_loan_details(loan_id, recent_only=True)[0]
            # if user != loan.borrower:
            #     raise HTTPException(
            #         status_code=400,
            #         detail="User must be the borrower"
            #     )

            # nano_address = loan.borrower_nano_address

            # return NanoAddressResponse(nano_address=nano_address)
            pass
