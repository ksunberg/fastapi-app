from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "usersss"  # <-- ТРИ 's' (usersss)
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    age = Column(Integer, nullable=False)
    is_subscribed = Column(Boolean, default=False)

class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    is_subscribed: bool

