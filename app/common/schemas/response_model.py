from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel


class ResponseModelBase(BaseModel):
    
    message: str
    success: bool = False
    data: Optional[Any] = None

class ResponseModel(ResponseModelBase):

    pass