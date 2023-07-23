"""Utils."""
import datetime
import json
import logging
import os
from typing import List
from typing_extensions import Unpack
from functools import wraps

from fastapi import Depends, HTTPException, Request, Response, status
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


class RouterUtils:
    """Router Utils."""

    @staticmethod
    def get_user_token(
        request: Request,
        res: Response,
        credential: HTTPAuthorizationCredentials = Depends(
            HTTPBearer(auto_error=False)
        )
    ) -> str:
        if credential is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Bearer authentication is needed",
                headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
            )
        try:
            if os.environ['NODE_ENV'] == 'development':
                # When using the Firebase Authentication emulator,
                # trust the UID in the decoded token.
                decoded_token = {'uid': request.headers.get('X-User-Uid')}
            else:
                decoded_token = auth.verify_id_token(credential.credentials)
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid authentication from Firebase. {err}",
                headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
            )

        res.headers['WWW-Authenticate'] = 'Bearer realm="auth_required"'
        return decoded_token['uid']

    @staticmethod
    def sanitize_output(data):
        for item in data:
            if 'loan_status' in item:
                item['loan_status'] = item['loan_status'].value

            if 'created' in item:
                item['created'] = item['created'].to_pydatetime()

            if 'offer_expiry' in item:
                item['offer_expiry'] = item['offer_expiry'].to_pydatetime()

        return data

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
