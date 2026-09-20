from pydantic import BaseModel

class ErrorResponse(BaseModel):
    status_code: int
    message: str
    error_code: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str