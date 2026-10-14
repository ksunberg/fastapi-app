from pydantic import BaseModel
from typing import Optional
from fastapi import status

class CustomExceptionA(Exception):
    def __init__(self, message: str = "Ошибка типа A"):
        self.message = message
        self.status_code = status.HTTP_400_BAD_REQUEST


class CustomExceptionB(Exception):
    def __init__(self, message: str = "Ресурс не найден"):
        self.message = message
        self.status_code = status.HTTP_404_NOT_FOUND


class ErrorResponse(BaseModel):
    error: str
    message: str
    status_code: int
    detail: Optional[str] = None