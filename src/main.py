from typing import Union
from fastapi import FastAPI
import schemas
import auth
import firebase_admin
from firebase_admin import firestore

db = firestore.client()
app = FastAPI()

""" loan create/read/update/delete endpoints """

@app.post("/loan")
async def submit_loan_application(user = Depends(auth.get_user_token), application: schemas.LoanApplication):
    return {"Hello": "World"}

@app.get("/loans")
async def get_loan_list(user = Depends(auth.get_user_token)):
    return {"Hello": "World"}

@app.get("/loan/{loan_id}")
async def get_loan_details(user = Depends(auth.get_user_token), loan_id: int):
    return {"Hello": "World"}

@app.put("/loan/{loan_id}")
async def update_loan(user = Depends(auth.get_user_token), loan_id: int):
    return {"Hello": "World"}

@app.delete("/loan/{loan_id}")
async def withdraw_loan_application(user = Depends(auth.get_user_token), loan_id: int):
    return {"Hello": "World"}

""" public loans endpoint for anonymized data """

@app.get("/loans")
async def get_public_loans():
    return {"Hello": "World"}

""" run various types of background checks as part of the application process """

@app.get("/check/{type}")
async def start_user_kyc(user = Depends(auth.get_user_token), type: schemas.checkType):
    return {"Hello": "World"}

""" savings account endpoints """

@app.get("/wallet/savings")
async def get_savings_wallet(user = Depends(auth.get_user_token)):
    return {"Hello": "World"}

@app.get("/savings/interest")
async def get_interest_payment_history(user = Depends(auth.get_user_token)):
    return {"Hello": "World"}

""" other wallet/payment related endpoints """

@app.get("/wallet/checking")
async def get_checking_wallet(user = Depends(auth.get_user_token)):
    return {"Hello": "World"}

@app.get("/wallet/payment")
async def get_bill_pay_wallet(user = Depends(auth.get_user_token)):
    return {"Hello": "World"}

@app.get("/withdaw/savings")
async def withdraw_from_savings(user = Depends(auth.get_user_token)):
    return {"Hello": "World"}

@app.get("/withdaw/checking")
async def withdraw_from_checking(user = Depends(auth.get_user_token)):
    return {"Hello": "World"}

@app.get("/transfer/savings")
async def transfer_from_savings_to_checking(user = Depends(auth.get_user_token)):
    return {"Hello": "World"}

@app.get("/transfer/checking")
async def transfer_from_checking_to_savings(user = Depends(auth.get_user_token)):
    return {"Hello": "World"}
