from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class User(BaseModel):
    username: str
    password: str
    role: Role

class UserCreate(BaseModel):
    username: str
    password: str
    role: Role

class Resource(BaseModel):
    id: int
    title: str
    content: str