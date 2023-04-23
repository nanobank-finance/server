from firebase_admin import firestore, auth, credentials, initialize_app
# from firebase.auth import # todo: start auth emulator properly on the server side
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Response
from src import FIREBASE_PROJECT_ID
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import json
import os

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
