"""Vouch Routes."""
import logging
from typing import Self

from bizlogic.vouch import VouchReader, VouchWriter

from fastapi import Depends, FastAPI

from ipfsclient.ipfs import Ipfs

from src.schemas import SuccessOrFailureResponse
from src.utils import ParserType, get_user_token
from src.utils import RouterUtils


LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class VouchRouter():
    """Vouch Router."""

    def __init__(self: Self, app: FastAPI) -> None:
        """Add routes for vouches.

        Args:
            app (FastAPI): Routes will be added to this app.
        """
        ipfsclient = Ipfs()
        vouch_reader = VouchReader(ipfsclient)

        # Loan application endpoints

        @app.post("/vouch", response_model=SuccessOrFailureResponse)
        async def submit_vouch(vouchee: str, user = Depends(get_user_token)):
            voucher = "123"  # TODO: get from KYC
            try:
                vouch_writer = VouchWriter(ipfsclient, voucher, vouchee)
                vouch_writer.write()

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
        
        @app.get("/vouch")
        async def get_all_vouches(recent: bool = False, user = Depends(get_user_token)):
            borrower = "123"  # TODO: get from KYC
            try:
                results = vouch_reader.get_all_vouches()
                return RouterUtils.parse_results(results, recent, ParserType.VOUCH)
            except Exception as e:
                LOG.exception(e)
                return SuccessOrFailureResponse(
                    success=False,
                    error_message=str(e),
                    error_type=type(e).__name__
                )
        
        @app.get("/vouch/user/self")
        async def get_my_vouchers(perspective: str = "voucher", recent: bool = False, user = Depends(get_user_token)):
            assert perspective in ["voucher", "vouchee"]  # TODO: handle invalid request properly (and make enum instead of str?)
            borrower = "123"  # TODO: get from KYC
            try:
                if perspective == "voucher":
                    results = vouch_reader.get_vouchers_for_borrower(borrower)
                elif perspective == "vouchee":
                    results = vouch_reader.get_vouchees_for_borrower(borrower)

                return RouterUtils.parse_results(results, recent, ParserType.VOUCH)
            except Exception as e:
                LOG.exception(e)
                return SuccessOrFailureResponse(
                    success=False,
                    error_message=str(e),
                    error_type=type(e).__name__
                )
            
        @app.get("/vouch/user/other")
        async def get_their_vouchers(them: str, perspective: str = "voucher", recent: bool = False, user = Depends(get_user_token)):
            assert perspective in ["voucher", "vouchee"]  # TODO: handle invalid request properly (and make enum instead of str?)
            try:
                if perspective == "voucher":
                    results = vouch_reader.get_vouchers_for_borrower(them)
                elif perspective == "vouchee":
                    results = vouch_reader.get_vouchees_for_borrower(them)

                return RouterUtils.parse_results(results, recent, ParserType.VOUCH)
            except Exception as e:
                LOG.exception(e)
                return SuccessOrFailureResponse(
                    success=False,
                    error_message=str(e),
                    error_type=type(e).__name__
                )
