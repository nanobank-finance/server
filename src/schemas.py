
from typing import Union
from pydantic import BaseModel


class SuccessOrFailResponse(BaseModel):
    success: bool
    error_message: Union[str, None] = None
    error_code: Union[int, None] = None
