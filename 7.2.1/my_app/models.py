from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class User(BaseModel):
    username: str
    password: str


class Base(DeclarativeBase):
    pass

class UserTable(Base):
    __tablename__ = "7_2_1"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

