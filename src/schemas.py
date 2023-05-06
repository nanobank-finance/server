"""Response type schemas."""
from typing import Union
from pydantic import BaseModel


class SuccessOrFailureResponse(BaseModel):
    """Model for operations that have no data response."""

    success: bool
    error_message: Union[str, None] = None
    error_type: Union[str, None] = None
