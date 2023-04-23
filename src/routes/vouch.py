from fastapi import Depends
import logging
from typing import List
import json
import datetime
from datetime import timezone
import pandas as pd
from src.schemas import SuccessOrFailResponse
from src.utils import get_user_token
from ipfsclient.ipfs import Ipfs
from ipfskvs.store import Store
from bizlogic.loan.reader import LoanReader
from bizlogic.loan.writer import LoanWriter
from bizlogic.vouch import VouchReader, VouchWriter


LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class VouchRouter():


    def nanosecond_epoch_to_datetime(self, timestamp):
        timestamp = int(timestamp)
        seconds = timestamp // 1000000000
        nanoseconds = timestamp % 1000000000
        return datetime.datetime.fromtimestamp(seconds) + datetime.timedelta(microseconds=nanoseconds // 1000)

    def get_most_recent(self, df, group_by):
        # Get the most recent data for each application

        # convert the "created" field to datetime format
        df['created'] = df['created'].apply(self.nanosecond_epoch_to_datetime)

        # group by "application" and get the row with the maximum "created" timestamp per group
        max_created_per_app = df.groupby(group_by)['created'].max().reset_index()

        # join the original dataframe with the grouped data to get the full row with the maximum "created" per application
        return pd.merge(df, max_created_per_app, on=[group_by, 'created'], how='inner')


    def __init__(self, app):

        ipfsclient = Ipfs()
        vouch_reader = VouchReader(ipfsclient)

        # Loan application endpoints

        @app.post("/vouch", response_model=SuccessOrFailResponse)
        async def submit_vouch(asking: int): #, user = Depends(get_user_token)):
            borrower = "123"  # TODO: get from KYC
            try:
                # vouch_writer = VouchWriter(ipfsclient, borrower, asking)
                # vouch_writer.write()
                pass
            except Exception as e:
                return SuccessOrFailResponse(
                    success=False,
                    error_message=str(e)
                )

            return SuccessOrFailResponse(
                success=True
            )
        
        @app.get("/vouch/user/voucher")
        async def get_my_vouchers(user = Depends(get_user_token), recent: bool = False):
            borrower = "123"  # TODO: get from KYC
            try:
                results = vouch_reader.get_vouchers_for_borrower(borrower)
            except Exception as e:
                return SuccessOrFailResponse(
                    success=False,
                    error_message=e
                )

            df = Store.to_dataframe(results, protobuf_parsers={
                "amount_asking": lambda store: store.reader.amount_asking,
                "closed": lambda store: store.reader.closed,
            })
            LOG.debug(df)
            if len(df) == 0:
                return []

            df.created = pd.to_numeric(df.created)
            if recent:
                df = self.get_most_recent(df, "application")

            return json.loads(df.to_json(orient="records"))

        @app.get("/vouch/user/vouchee")
        async def get_my_vouchees(user = Depends(get_user_token), recent: bool = False):
            borrower = "123"  # TODO: get from KYC
            try:
                results = vouch_reader.get_vouchers_for_borrower(borrower)
            except Exception as e:
                return SuccessOrFailResponse(
                    success=False,
                    error_message=e
                )

            df = Store.to_dataframe(results, protobuf_parsers={
                "amount_asking": lambda store: store.reader.amount_asking,
                "closed": lambda store: store.reader.closed,
            })
            LOG.debug(df)
            if len(df) == 0:
                return []

            df.created = pd.to_numeric(df.created)
            if recent:
                df = self.get_most_recent(df, "application")

            return json.loads(df.to_json(orient="records"))
