from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    password: str

class Base(DeclarativeBase):
    pass

class UserTable(Base):
    __tablename__ = "pytest711"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)