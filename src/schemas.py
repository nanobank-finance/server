"""Response type schemas."""
from typing import Union, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class SuccessOrFailureResponse(BaseModel):
    """Model for operations that have no data response."""

    success: bool
    error_message: Union[str, None] = None
    error_type: Union[str, None] = None

class LoanApplication(BaseModel):
    asking: int

class SumsubReviewResult(BaseModel):
    moderationComment: Optional[str] = Field(None, description="A human-readable comment that can be shown to the end user.")
    clientComment: Optional[str] = Field(None, description="A human-readable comment that should not be shown to the end user.")
    reviewAnswer: Optional[str] = Field(None, description="Has an impact on an applicant only with reviewStatus: completed.")
    rejectLabels: Optional[List[str]] = Field(None, description="Labels explaining the reason of rejection.")
    reviewRejectType: Optional[str] = Field(None, description="Type of rejection. Possible values: `FINAL` or `RETRY`")


class SumsubApplicantStatus(BaseModel):
    createDate: datetime = Field(None, description="Date of creation of the applicant.")
    reviewDate: Optional[datetime] = Field(None, description="Date of check ended.")
    startDate: Optional[datetime] = Field(None, description="Date of check started.")
    reviewResult: Optional[SumsubReviewResult] = Field(None, description="The result of the review.")
    reviewStatus: str = Field(None, description="Current status of an applicant.")
