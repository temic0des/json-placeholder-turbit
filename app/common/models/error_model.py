from typing import Any
from pydantic import BaseModel


class ErrorResponseModel(BaseModel):

    details: Any = None
    message: str
    code: str