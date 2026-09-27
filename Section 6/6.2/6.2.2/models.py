from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
import re

class ProblemDetails(BaseModel):
    type: str = "https://example.com/problems/validation-error"
    title: str = "Validation Error"
    status: int = 422
    detail: str = "The request body failed validation."
    instance: str
    errors: Optional[List[dict]] = None


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    age: int = Field(..., gt=18)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=16)
    phone: Optional[str] = None

    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Имя пользователя должно содержать только латинские буквы, цифры и подчеркивание')
        return v

    @validator('phone')
    def validate_phone(cls, v):
        if v is not None and not re.match(r'^\+?[0-9]{10,15}$', v):
            raise ValueError('Номер телефона должен содержать от 10 до 15 цифр')
        return v


class UserResponse(BaseModel):
    id: int
    username: str