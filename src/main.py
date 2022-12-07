from typing import Union
from fastapi import FastAPI
import schemas
import firebase_admin
from firebase_admin import firestore

db = firestore.client()
app = FastAPI()

# todo: request decorator to check id_token and mark private vs public endpoints easier

""" loan create/read/update/delete endpoints """

@app.post("/user/{uid}/loan")
async def submit_loan_application(uid: str, id_token: str, application: schemas.LoanApplication):
    return {"Hello": "World"}

@app.get("/user/{uid}/loans")
async def get_loan_list(uid: str, id_token: str):
    return {"Hello": "World"}

@app.get("/user/{uid}/loan/{loan_id}")
async def get_loan_details(uid: str, loan_id: int, id_token: str):
    return {"Hello": "World"}

@app.put("/user/{uid}/loan/{loan_id}")
async def update_loan(uid: str, loan_id: int, id_token: str):
    return {"Hello": "World"}

@app.delete("/user/{uid}/loan/{loan_id}")
async def withdraw_loan_application(uid: str, loan_id: int, id_token: str):
    return {"Hello": "World"}

""" public loans endpoint for anonymized data """

@app.get("/loans")
async def get_public_loans():
    return {"Hello": "World"}

""" run various types of background checks as part of the application process """

@app.get("/user/{uid}/check/{type}")
async def start_user_kyc(uid: str, type: schemas.checkType, id_token: str):
    return {"Hello": "World"}

""" savings account endpoints """

@app.get("/user/{uid}/savings")
async def get_savings_wallet(uid: str, id_token: str):
    return {"Hello": "World"}

@app.get("/user/{uid}/savings/interest")
async def get_interest_payment_history(uid: str, id_token: str):
    return {"Hello": "World"}

""" other wallet/payment related endpoints """

@app.get("/user/{uid}/checking")
async def get_checking_wallet(uid: str, id_token: str):
    return {"Hello": "World"}

@app.get("/user/{uid}/pay")
async def get_bill_pay_wallet(uid: str, id_token: str):
    return {"Hello": "World"}

@app.get("/user/{uid}/withdaw/savings")
async def withdraw_from_savings(uid: str, id_token: str):
    return {"Hello": "World"}

@app.get("/user/{uid}/withdaw/checking")
async def withdraw_from_checking(uid: str, id_token: str):
    return {"Hello": "World"}

@app.get("/user/{uid}/transfer/savings")
async def transfer_from_savings_to_checking(uid: str, id_token: str):
    return {"Hello": "World"}

@app.get("/user/{uid}/transfer/checking")
async def transfer_from_checking_to_savings(uid: str, id_token: str):
    return {"Hello": "World"}
