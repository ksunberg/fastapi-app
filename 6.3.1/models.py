from fastapi import status
from pydantic import BaseModel

class ErrorResponseModel(BaseModel):
    status_code: int
    message: str
    error_code: str


class UserNotFoundException(Exception):
    def __init__(self, message: str = "Пользователь не найден"):
        self.message = message
        self.error_code = "USER_NOT_FOUND"
        self.status_code = status.HTTP_404_NOT_FOUND


class InvalidUserDataException(Exception):
    def __init__(self, message: str = "Неверные данные пользователя"):
        self.message = message
        self.error_code = "INVALID_USER_DATA"
        self.status_code = status.HTTP_400_BAD_REQUEST


class UserExistsException(Exception):
    def __init__(self, message: str = "Пользователь уже существует"):
        self.message = message
        self.error_code = "USER_EXISTS"
        self.status_code = status.HTTP_409_CONFLICT


users_db = {}
