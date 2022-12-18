from typing import Union, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import firestore, auth, credentials, initialize_app
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Response
from dotenv import load_dotenv
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
load_dotenv(Path(os.environ['SECRETS_PATH']+"/.env.nanobank"))
initialize_app(credential=credentials.Certificate(os.environ['FIREBASE_CREDENTIALS_PATH']))

# database
db = firestore.client()

wallet_status_table = db.collection(u'wallet_status')
loan_application_status_table = db.collection(u'loan_application_status')
loan_payment_status_table = db.collection(u'loan_payment_status')
wallet_table = db.collection(u'wallet')
user_table = db.collection(u'user')
loan_table = db.collection(u'loan')
stake_table = db.collection(u'stake')
loan_payment_table = db.collection(u'loan_payment_event')


# feature store config
config = utils.get_config()

class SuccessOrFailResponse(BaseModel):
    success: bool
    error_message: Union[str, None] = None
    error_code: Union[int, None] = None

class TokenResponse(BaseModel):
    token: str

# WIP
""" sumsub token for kyc and verification """
@app.get("/sumsub", response_model=TokenResponse)
async def get_sumsub_token(user = Depends(utils.get_user_token)):
    applicant_id = sumsub.create_applicant(user['uid'], 'basic-kyc-level')
    image_id = sumsub.add_document(applicant_id)
    status = sumsub.get_applicant_status(applicant_id)
    token = sumsub.get_access_token(user['uid'], 'basic-kyc-level')
    return {
        "token": token
    }

""" loan application create/read/update/delete endpoints """

# TODO
@app.post("/loan", response_model=SuccessOrFailResponse)
async def submit_loan_application(application: schemas.Loan, user = Depends(utils.get_user_token)):
    return {"Hello": "World"}

# TODO
@app.get("/loans", response_model=List[schemas.Loan])
async def get_loan_list(user = Depends(utils.get_user_token)):
    return {"Hello": "World"}

# WIP
@app.get("/loan/{loan_id}", response_model=Union[schemas.Loan, SuccessOrFailResponse])
async def get_loan_details(loan_id: int, user = Depends(utils.get_user_token)):
    # TODO: check if user owns the loan?
    loan = loan_ref.where(u'loan_id', u'==', loan_id).get()
    if loan.exists:
        return { "status": {"success": True}, "data": loan.to_dict() }
    
    return { "status": {"success": False, "error_code": 404, "error_message": "loan not found"} }

# TODO
@app.put("/loan/{loan_id}", response_model=SuccessOrFailResponse)
async def update_loan_application(application: schemas.Loan, user = Depends(utils.get_user_token)):
    return {"Hello": "World"}

# TODO
@app.delete("/loan/{loan_id}", response_model=SuccessOrFailResponse)
async def withdraw_loan_application(loan_id: int, user = Depends(utils.get_user_token)):
    return {"Hello": "World"}

""" public loans endpoint for anonymized data """

# TODO
@app.get("/loans", response_model=List[schemas.Loan])
async def get_public_loans():
    return {"Hello": "World"}

""" wallet endpoints """

# WIP
@app.get("/wallets", response_model=List[schemas.Wallet])
async def get_wallets(): #user = Depends(utils.get_user_token)):
    data = wallet_table.get() #where()
    response = []
    for doc in data:
        print(doc.to_dict())
        response.append(schemas.Wallet.from_dict(doc.to_dict()))
    
    return response
