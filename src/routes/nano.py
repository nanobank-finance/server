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
