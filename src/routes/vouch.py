from fastapi import Depends
import logging
from typing import List
import json
import datetime
from datetime import timezone
import pandas as pd
from src.schemas import SuccessOrFailResponse
from src.utils import ParserType, get_user_token
from ipfsclient.ipfs import Ipfs
from ipfskvs.store import Store
from bizlogic.loan.reader import LoanReader
from bizlogic.loan.writer import LoanWriter
from bizlogic.vouch import VouchReader, VouchWriter
from src.utils import RouterUtils


LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class VouchRouter():

    def __init__(self, app):

        ipfsclient = Ipfs()
        vouch_reader = VouchReader(ipfsclient)

        # Loan application endpoints

        @app.post("/vouch", response_model=SuccessOrFailResponse)
        async def submit_vouch(vouchee: str, user = Depends(get_user_token)):
            voucher = "123"  # TODO: get from KYC
            try:
                vouch_writer = VouchWriter(ipfsclient, voucher, vouchee)
                vouch_writer.write()

                return SuccessOrFailResponse(
                    success=True
                )
            except Exception as e:
                return SuccessOrFailResponse(
                    success=False,
                    error_message=str(e)
                )
        
        @app.get("/vouch/user/voucher")
        async def get_my_vouchers(recent: bool = False, user = Depends(get_user_token)):
            borrower = "123"  # TODO: get from KYC
            try:
                results = vouch_reader.get_vouchers_for_borrower(borrower)
                return RouterUtils.parse_results(results, recent, ParserType.VOUCH)
            except Exception as e:
                return SuccessOrFailResponse(
                    success=False,
                    error_message=str(e)
                )

        @app.get("/vouch/user/vouchee")
        async def get_my_vouchees(recent: bool = False, user = Depends(get_user_token)):
            borrower = "123"  # TODO: get from KYC
            try:
                results = vouch_reader.get_vouchers_for_borrower(borrower)
                return RouterUtils.parse_results(results, recent, ParserType.VOUCH)
            except Exception as e:
                return SuccessOrFailResponse(
                    success=False,
                    error_message=str(e)
                )
