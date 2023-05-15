"""Vouch Routes."""
import logging
from typing import List, Self, Union

from bizlogic.vouch import VouchReader, VouchWriter
from bizlogic.utils import ParserType, Utils

from fastapi import Depends, FastAPI

from ipfsclient.ipfs import Ipfs

from src.schemas import SuccessOrFailureResponse
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
        async def submit_vouch(
            vouchee: str,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> SuccessOrFailureResponse:
            """Create a vouch.

            Args:
                vouchee (str): The user to vouch for.

            Returns:
                SuccessOrFailureResponse: `success=True` when successful.
            """
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

        @app.get(
            "/vouch",
            response_model=List
        )
        async def get_all_vouches(
            recent: bool = False,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> List:
            """Get all vouches.

            Args:
                recent (bool, optional): Whether to only get recent vouches. Defaults to False.
            
            Returns:
                List: List of vouches.
            """
            return vouch_reader.get_all_vouches()

        @app.get(
            "/vouch/user/self",
            response_model=List
        )
        async def get_my_vouchers(
            perspective: str = "voucher",
            recent: bool = False,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> List:
            """Get all vouches for the current user.

            Args:
                perspective (str, optional): Whether to get vouchers or vouchees. Defaults to "voucher".
                recent (bool, optional): Whether to only get recent vouches. Defaults to False.

            Returns:
                List: List of vouches.
            """
            assert perspective in ["voucher", "vouchee"]  # TODO: handle invalid request properly (and make enum instead of str?)  # noqa: E501
            borrower = "123"  # TODO: get from KYC
            if perspective == "voucher":
                return vouch_reader.query_vouches(voucher=borrower)
            elif perspective == "vouchee":
                return vouch_reader.query_vouches(vouchee=borrower)

        @app.get(
            "/vouch/user/other",
            response_model=List
        )
        async def get_their_vouchers(
            them: str,
            perspective: str = "voucher",
            recent: bool = False,
            user: str = Depends(RouterUtils.get_user_token)
        ) -> List:
            """Get all vouches for the given user.

            Args:
                them (str): The user to get vouches for.
                perspective (str, optional): Whether to get vouchers or vouchees. Defaults to "voucher".
                recent (bool, optional): Whether to only get recent vouches. Defaults to False.

            Returns:
                List: List of vouches.
            """
            assert perspective in ["voucher", "vouchee"]  # TODO: handle invalid request properly (and make enum instead of str?)  # noqa: E501
            if perspective == "voucher":
                results = vouch_reader.get_vouchers_for_borrower(them)
            elif perspective == "vouchee":
                results = vouch_reader.get_vouchees_for_borrower(them)

            return Utils.parse_results(
                results,
                recent,
                ParserType.VOUCH
            )
