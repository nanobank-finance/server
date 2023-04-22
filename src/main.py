from typing import Union, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import auth, credentials, initialize_app
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Response
from dotenv import load_dotenv
from dataclasses import dataclass, asdict
from dacite import from_dict
from typing import Union, TypeVar, Generic
from pydantic import BaseModel
from enum import Enum
from pathlib import Path
import os
import schemas
import utils
import sumsub

# server setup
app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# firebase auth credentials
load_dotenv(Path(os.environ['SECRETS_PATH']+"/.env.nanoswap"))
initialize_app(credential=credentials.Certificate(os.environ['FIREBASE_CREDENTIALS_PATH']))

# feature store config
config = utils.get_config()


# class TokenResponse(BaseModel):
#     token: str
# 
# WIP
# """ sumsub token for kyc and verification """
# @app.get("/sumsub", response_model=TokenResponse)
# async def get_sumsub_token(user = Depends(utils.get_user_token)):
#     applicant_id = sumsub.create_applicant(user['uid'], 'basic-kyc-level')
#     image_id = sumsub.add_document(applicant_id)
#     status = sumsub.get_applicant_status(applicant_id)
#     token = sumsub.get_access_token(user['uid'], 'basic-kyc-level')
#     return {
#         "token": token
#     }

