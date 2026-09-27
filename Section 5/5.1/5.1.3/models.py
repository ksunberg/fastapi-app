from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password_hash: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    user_id: int


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    user_id: Optional[int] = None


class TodoResponse(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True