"""Response type schemas."""
from typing import Union, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class SuccessOrFailureResponse(BaseModel):
    """
    Model for operations that have no data response.
    
    This is used when an operation either fails or succeeds without producing data.
    """
    success: bool = Field(..., description="A boolean value indicating whether the operation was successful.")
    error_message: Optional[str] = Field(None, description="An error message that explains why the operation failed, if it failed.")
    error_type: Optional[str] = Field(None, description="The type of error, if an error occurred.")


class LoanApplication(BaseModel):
    """
    Model representing a loan application.

    This model only includes the asking price of the loan.
    """
    asking: int = Field(..., description="The asking amount of the loan.")


class LoanOffer(BaseModel):
    """
    Model representing a loan offer.

    This includes information about the borrower, principal amount, interest rate, number of payments, 
    start date, maturity date, and expiry date of the loan offer.
    """
    borrower: str = Field(..., description="The identifier of the borrower.")
    principal: float = Field(..., description="The principal amount of the loan.")
    interest: float = Field(..., description="The interest rate of the loan.")
    payments: int = Field(..., description="The number of payments for the loan.")
    start: datetime = Field(..., description="The start date of the loan.")
    maturity: datetime = Field(..., description="The maturity date of the loan.")
    expiry: datetime = Field(..., description="The expiry date of the loan offer.")


class LoanStatusType(Enum):
    """
    Enum representing the status of the loan.

    The status can be 'pending acceptance', 'expired unaccepted', and 'accepted'.
    """
    PENDING_ACCEPTANCE = 1
    EXPIRED_UNACCEPTED = 2
    ACCEPTED = 3


class LoanResponse(BaseModel):
    """
    Model representing a loan.

    This includes information about the loan ID, borrower, lender, creation time, principal amount, 
    offer expiry time, transaction ID, acceptance status, number of payments, and loan status.
    """
    loan: str = Field(..., description="The identifier of the loan.")
    borrower: str = Field(..., description="The identifier of the borrower.")
    lender: str = Field(..., description="The identifier of the lender.")
    created: datetime = Field(..., description="The time when the loan was created.")
    principal: int = Field(..., description="The principal amount of the loan.")
    offer_expiry: datetime = Field(..., description="The time when the loan offer expires.")
    transaction: Optional[str] = Field(None, description="The transaction ID associated with the loan.")
    accepted: bool = Field(..., description="A boolean value indicating whether the loan has been accepted.")
    payments: int = Field(..., description="The number of payments for the loan.")
    loan_status: LoanStatusType = Field(..., description="The status of the loan.")


class RepaymentSchedule(BaseModel):
    """
    Model representing a repayment schedule.

    This includes the payment ID, amount due, and due date for each payment.
    """
    paymentId: str = Field(..., description="The unique identifier for the payment.")
    amountDue: int = Field(..., description="The amount due for the payment.")
    dueDate: datetime = Field(..., description="The date and time when the payment is due.")


class Metadata(BaseModel):
    """
    Model representing the metadata associated with the loan.

    This includes the borrower, lender, loan, and created.
    """
    borrower: str = Field(..., description="The identifier of the borrower.")
    lender: str = Field(..., description="The identifier of the lender.")
    loan: str = Field(..., description="The identifier of the loan.")
    created: datetime = Field(..., description="The timestamp of when the loan was created.")


class LoanDetailResponse(BaseModel):
    """
    Model representing the detailed information of a loan.

    This includes principal amount, repayment schedule, offer expiry and metadata.
    """
    principalAmount: int = Field(..., description="The principal amount of the loan.")
    repaymentSchedule: List[RepaymentSchedule] = Field([], description="The repayment schedule of the loan.")
    offerExpiry: datetime = Field(..., description="The date and time when the loan offer expires.")
    metadata: Metadata = Field(..., description="The metadata associated with the loan.")


class SumsubReviewResult(BaseModel):
    """
    Model representing the result of the KYC review.

    This includes the moderation comment, client comment, review answer, reject labels, and review reject type.
    """
    moderationComment: Optional[str] = Field(None, description="A human-readable comment that can be shown to the end user.")
    clientComment: Optional[str] = Field(None, description="A human-readable comment that should not be shown to the end user.")
    reviewAnswer: Optional[str] = Field(None, description="Has an impact on an applicant only with reviewStatus: completed.")
    rejectLabels: Optional[List[str]] = Field(None, description="Labels explaining the reason of rejection.")
    reviewRejectType: Optional[str] = Field(None, description="Type of rejection. Possible values: `FINAL` or `RETRY`")


class SumsubApplicantStatus(BaseModel):
    """
    Model representing the status of the applicant.

    This includes the creation date, review date, start date, review result, and review status.
    """
    createDate: datetime = Field(None, description="Date of creation of the applicant.")
    reviewDate: Optional[datetime] = Field(None, description="Date of check ended.")
    startDate: Optional[datetime] = Field(None, description="Date of check started.")
    reviewResult: Optional[SumsubReviewResult] = Field(None, description="The result of the review.")
    reviewStatus: str = Field(None, description="Current status of an applicant.")
