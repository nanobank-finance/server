from typing import Union, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import firestore, auth, credentials, initialize_app
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Response
from dotenv import load_dotenv
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
loan_ref = db.collection(u'loan')

# feature store config
config = utils.get_config()

# WIP
""" sumsub token for kyc and verification """
@app.get("/sumsub", response_model=schemas.TokenResponse)
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
@app.post("/loan", response_model=schemas.SuccessOrFailResponse)
async def submit_loan_application(application: schemas.LoanApplicationModel, user = Depends(utils.get_user_token)):
    return {"Hello": "World"}

# TODO
@app.get("/loans", response_model=List[schemas.LoanApplicationModel])
async def get_loan_list(user = Depends(utils.get_user_token)):
    return {"Hello": "World"}

# WIP
@app.get("/loan/{loan_id}", response_model=Union[schemas.LoanApplicationModel, schemas.SuccessOrFailResponse])
async def get_loan_details(loan_id: int, user = Depends(utils.get_user_token)):
    # TODO: check if user owns the loan?
    loan = loan_ref.where(u'loan_id', u'==', loan_id).get()
    if loan.exists:
        return { "status": {"success": True}, "data": loan.to_dict() }
    
    return { "status": {"success": False, "error_code": 404, "error_message": "loan not found"} }

# TODO
@app.put("/loan/{loan_id}", response_model=schemas.SuccessOrFailResponse)
async def update_loan_application(application: schemas.LoanApplicationModel, user = Depends(utils.get_user_token)):
    return {"Hello": "World"}

# TODO
@app.delete("/loan/{loan_id}", response_model=schemas.SuccessOrFailResponse)
async def withdraw_loan_application(loan_id: int, user = Depends(utils.get_user_token)):
    return {"Hello": "World"}

""" public loans endpoint for anonymized data """

# TODO
@app.get("/loans", response_model=List[schemas.LoanApplicationModel])
async def get_public_loans():
    return {"Hello": "World"}

""" run various types of background checks as part of the application process """

# TODO
@app.get("/check/{type}", response_model=schemas.SuccessOrFailResponse)
async def start_user_kyc(type: schemas.CheckType, user = Depends(utils.get_user_token)):
    return {"Hello": "World"}

""" savings account endpoints """

# WIP
@app.get("/wallets", response_model=List[schemas.WalletModel])
async def get_savings_wallet(): #user = Depends(utils.get_user_token)):
    return [
        {
            "name": "wallet 1",
            "address": "address 123",
            "type": schemas.WalletType.PERSONAL,
            "is_frozen": False
        },
        {
            "name": "wallet 2",
            "address": "address 123",
            "type": schemas.WalletType.PERSONAL,
            "is_frozen": False
        },
        {
            "name": "wallet 3",
            "address": "address 123",
            "type": schemas.WalletType.PERSONAL,
            "is_frozen": True,
            "frozen_reason": "pending stake for loan 12345",
            "frozen_reason_code": 102
        },
        {
            "name": "payment for loan 123141",
            "address": "address 123",
            "type": schemas.WalletType.PAYMENT,
            "is_frozen": False
        },
        {
            "name": "yield from loan 12354",
            "address": "address 123",
            "type": schemas.WalletType.YIELD,
            "is_frozen": False
        },
    ]

# TODO
@app.get("/savings/interest", response_model=schemas.SavingsInterestModel)
async def get_interest_payment_history(user = Depends(utils.get_user_token)):
    return {"Hello": "World"}

""" other wallet/payment related endpoints """

# TODO
@app.get("/wallet/checking", response_model=schemas.WalletModel)
async def get_checking_wallet(user = Depends(utils.get_user_token)):
    return {"Hello": "World"}

# TODO
@app.get("/wallet/payment", response_model=schemas.WalletModel)
async def get_bill_pay_wallet(user = Depends(utils.get_user_token)):
    return {"Hello": "World"}

# TODO
@app.get("/withdraw/savings", response_model=schemas.SuccessOrFailResponse)
async def withdraw_from_savings(user = Depends(utils.get_user_token)):
    return {"Hello": "World"}

# TODO
@app.get("/withdraw/checking", response_model=schemas.SuccessOrFailResponse)
async def withdraw_from_checking(user = Depends(utils.get_user_token)):
    return {"Hello": "World"}

# TODO
@app.get("/transfer/savings", response_model=schemas.SuccessOrFailResponse)
async def transfer_from_savings_to_checking(user = Depends(utils.get_user_token)):
    return {"Hello": "World"}

# TODO
@app.get("/transfer/checking", response_model=schemas.SuccessOrFailResponse)
async def transfer_from_checking_to_savings(user = Depends(utils.get_user_token)):
    return {"Hello": "World"}
