from firebase_admin import firestore, auth, credentials, initialize_app
# from firebase.auth import # todo: start auth emulator properly on the server side
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Response
import datetime
from src import FIREBASE_PROJECT_ID
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from ipfskvs.store import Store
import json
import os
import logging
import pandas as pd
from enum import Enum


LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class ParserType:
    LOAN_APPLICATION = 1
    LOAN = 2
    VOUCH = 3


PARSERS = {
    ParserType.LOAN_APPLICATION: {
        "amount_asking": lambda store: store.reader.amount_asking,
        "closed": lambda store: store.reader.closed,
    },
    ParserType.LOAN: {
        "principal": lambda store: store.reader.principal_amount,
        "offer_expiry": lambda store: datetime.datetime.fromtimestamp(store.reader.offer_expiry.seconds + store.reader.offer_expiry.nanos/1e9),
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

    @staticmethod
    def nanosecond_epoch_to_datetime(timestamp):
        timestamp = int(timestamp)
        seconds = timestamp // 1000000000
        nanoseconds = timestamp % 1000000000
        return datetime.datetime.fromtimestamp(seconds) + datetime.timedelta(microseconds=nanoseconds // 1000)

    @staticmethod
    def get_most_recent(df, group_by):
        # Get the most recent data for each application

        # convert the "created" field to datetime format
        df['created'] = df['created'].apply(RouterUtils.nanosecond_epoch_to_datetime)

        # group by "application" and get the row with the maximum "created" timestamp per group
        max_created_per_app = df.groupby(group_by)['created'].max().reset_index()

        # join the original dataframe with the grouped data to get the full row with the maximum "created" per application
        return pd.merge(df, max_created_per_app, on=[group_by, 'created'], how='inner')

    @staticmethod
    def parse_results(data, recent, parser_type):
        df = Store.to_dataframe(data, protobuf_parsers=PARSERS[parser_type])
        LOG.debug(df)
        if len(df) == 0:
            return []

        df.created = pd.to_numeric(df.created)
        if recent:
            df = RouterUtils.get_most_recent(df, GROUP_BY[parser_type])

        return json.loads(df.to_json(orient="records"))

# other utils

def get_user_token(res: Response, credential: HTTPAuthorizationCredentials=Depends(
            HTTPBearer(auto_error=False)
        )):
    
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

def get_config():
    scopes = [
        "https://www.googleapis.com/auth/firebase.remoteconfig"
    ]

    # Authenticate a credential with the service account
    credentials = service_account.Credentials.from_service_account_file(
        os.environ['FIREBASE_CREDENTIALS_PATH'], scopes=scopes)

    authed_session = AuthorizedSession(credentials)
    # https://firebase.google.com/docs/reference/remote-config/rest/v1/projects/getRemoteConfig
    url = f"https://firebaseremoteconfig.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/remoteConfig"
    response = authed_session.get(url)
    response = json.loads(response.content.decode('utf-8'))
    response = response.get("parameters")

    feature_flags = []
    for flag in response.keys():
        if response.get(flag).get('valueType') == 'BOOLEAN':
            default_value = bool(response.get(flag).get('defaultValue').get('value'))

    print(response)
