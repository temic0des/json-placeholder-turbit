from typing import Any
from fastapi import HTTPException


class JsonPlaceholderException(HTTPException):

    def __init__(self, status_code: int, detail: Any = None, code: str = None) -> None:
        super().__init__(status_code, detail)
        self.code = code

    def dict(self):
        return {
            "status_code": self.status_code,
            "detail": self.detail,
            "code": self.code
        }