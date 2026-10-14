from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "tasks2_2_1"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]

class UserPost(BaseModel):
    username: str

class UserRead(BaseModel):
    id: int
    username: str