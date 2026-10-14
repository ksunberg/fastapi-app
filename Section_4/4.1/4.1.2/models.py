from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel

class Base(DeclarativeBase):
    pass

class UserTable(Base):
    __tablename__ = "usertable1"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)  # Вместо password

class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str
    password: str

