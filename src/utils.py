"""Utils."""
import datetime
import json
import logging
import os
from typing import List
from typing_extensions import Unpack
from functools import wraps

from fastapi import Depends, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from firebase_admin import auth

from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

from ipfskvs.store import Store

import pandas as pd

from src import FIREBASE_PROJECT_ID
from src.schemas import SuccessOrFailureResponse


LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class ParserType:
    """The type of protobuf object."""

    LOAN_APPLICATION = 1
    LOAN = 2
    VOUCH = 3


def parse_offer_expiry(store: Store) -> datetime.date:
    """Get the offer expiry timestamp as a datetime.

    Args:
        store (Store): The store object to parse

    Returns:
        datetime.date: The offer expiry
    """
    return datetime.datetime.fromtimestamp(
        store.reader.offer_expiry.seconds + store.reader.offer_expiry.nanos / 1e9  # noqa: E501
    )


PARSERS = {
    ParserType.LOAN_APPLICATION: {
        "amount_asking": lambda store: store.reader.amount_asking,
        "closed": lambda store: store.reader.closed,
    },
    ParserType.LOAN: {
        "principal": lambda store: store.reader.principal_amount,
        "offer_expiry": parse_offer_expiry,
        "transaction": lambda store: store.reader.transaction,
        "accepted": lambda store: store.reader.accepted,
        "payments": lambda store: len(store.reader.repayment_schedule)
    },
    ParserType.VOUCH: {
        "voucher": lambda store: store.reader.voucher
    }
}

GROUP_BY = {
    ParserType.LOAN_APPLICATION: 'application',
    ParserType.LOAN: 'loan',
    ParserType.VOUCH: 'vouch'
}


class RouterUtils:
    """Router Utils."""
    @staticmethod
    def nanosecond_epoch_to_datetime(timestamp: int) -> datetime.date:
        """Convert nano seconds since epoch to date.

        Args:
            timestamp (int): Count of nanoseconds since 1970 Jan 1

        Returns:
            datetime.date: The date corresponding to the timestamp
        """
        timestamp = int(timestamp)
        seconds = timestamp // 1000000000
        nanoseconds = timestamp % 1000000000
        return datetime.datetime.fromtimestamp(
            seconds
        ) + datetime.timedelta(
            microseconds=nanoseconds // 1000
        )

    @staticmethod
    def get_most_recent(df: pd.DataFrame, group_by: str) -> pd.DataFrame:
        """Filter a CDC dataframe to get only the most recent of each object.

        Args:
            df (pd.DataFrame): The dataframe to filter
            group_by (str): The object id to group by

        Returns:
            pd.DataFrame: The filtered dataframe
        """
        # convert the "created" field to datetime format
        df['created'] = df['created'].apply(
            RouterUtils.nanosecond_epoch_to_datetime
        )

        # group by application|loan|vouch
        # and get the row with the maximum "created" timestamp per group
        max_created_per_app = df.groupby(
            group_by
        )['created'].max().reset_index()

        # join the original dataframe with the grouped data
        # to get the full row with the maximum "created" per application
        return pd.merge(
            df,
            max_created_per_app,
            on=[group_by, 'created'],
            how='inner'
        )

    @staticmethod
    def parse_results(data: List, recent: bool, parser_type: int) -> dict:
        """Parse the results.

        Args:
            data (List): _description_
            recent (bool): _description_
            parser_type (int): _description_

        Returns:
            Any: _description_
        """
        LOG.debug(data)
        LOG.debug("parsers %s:", PARSERS[parser_type])
        df = Store.to_dataframe(data, protobuf_parsers=PARSERS[parser_type])
        LOG.debug(df)
        if len(df) == 0:
            return []

        df.created = pd.to_numeric(df.created)
        if recent:
            df = RouterUtils.get_most_recent(df, GROUP_BY[parser_type])

        return json.loads(df.to_json(orient="records"))

    @staticmethod
    def get_user_token(
        res: Response,
        credential: HTTPAuthorizationCredentials = Depends(
            HTTPBearer(auto_error=False)
        )
    ) -> None:
        """Work in progress."""
        return

        if credential is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Bearer authentication is needed",
                headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
            )
        try:
            if os.environ['NODE_ENV'] == 'development':
                # ??????
                auth.useEmulator("http://localhost:9099")
                decoded_token = auth.verify_id_token(credential.credentials)
            else:
                decoded_token = auth.verify_id_token(credential.credentials)
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid authentication from Firebase. {err}",
                headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
            )

        res.headers['WWW-Authenticate'] = 'Bearer realm="auth_required"'
        return decoded_token


def get_config() -> None:
    """Get the feature flag config."""
    scopes = [
        "https://www.googleapis.com/auth/firebase.remoteconfig"
    ]

    # Authenticate a credential with the service account
    credentials = service_account.Credentials.from_service_account_file(
        os.environ['FIREBASE_CREDENTIALS_PATH'], scopes=scopes)

    authed_session = AuthorizedSession(credentials)
    # https://firebase.google.com/docs/reference/remote-config/rest/v1/projects/getRemoteConfig
    url = f"https://firebaseremoteconfig.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/remoteConfig"  # noqa: E501
    response = authed_session.get(url)
    response = json.loads(response.content.decode('utf-8'))
    response = response.get("parameters")

    # feature_flags = []
    # for flag in response.keys():
    #     if response.get(flag).get('valueType') == 'BOOLEAN':
    #         default_value = bool(response.get(flag).get('defaultValue').get('value'))  # noqa: E501

    print(response)
