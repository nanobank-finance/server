
# Loan application endpoints

@app.post("/loan/application", response_model=SuccessOrFailResponse)
async def submit_loan_application(application: schemas.Loan, user = Depends(utils.get_user_token)):
    return {"Hello": "World"}

@app.delete("/loan/application/{loan_id}", response_model=SuccessOrFailResponse)
async def withdraw_loan_application(loan_id: int, user = Depends(utils.get_user_token)):
    return {"Hello": "World"}


# Loan endpoints

# TODO
@app.get("/loans", response_model=List[schemas.Loan])
async def get_all_loans(user = Depends(utils.get_user_token)):
    return {"Hello": "World"}


# TODO
@app.get("/loans/user", response_model=List[schemas.Loan])
async def get_my_loans(user = Depends(utils.get_user_token)):
    return {"Hello": "World"}

# WIP
@app.get("/loan/{loan_id}", response_model=Union[schemas.Loan, SuccessOrFailResponse])
async def get_loan_details(loan_id: int, user = Depends(utils.get_user_token)):
    # loan = loan_ref.where(u'loan_id', u'==', loan_id).get()
    # if loan.exists:
    #     return { "status": {"success": True}, "data": loan.to_dict() }
    
    # return { "status": {"success": False, "error_code": 404, "error_message": "loan not found"} }
    return {"Hello": "World"}
