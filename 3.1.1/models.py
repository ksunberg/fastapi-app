from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel, EmailStr

class Base(DeclarativeBase):
    pass

class Table(Base):
    __tablename__ = "userss"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    email: Mapped[str]
    age: Mapped[int] = mapped_column(nullable=True)
    is_subscribed: Mapped[bool] = mapped_column(default=False)

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int = None
    is_subscribed: bool = False

