from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel
from typing import Optional

class Base(DeclarativeBase):
    pass

class TodoTable(Base):
    __tablename__ = "todos"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    completed: Mapped[bool] = mapped_column(default=False)

class TodoCreate(BaseModel):
    title: str
    description: str


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    class Config:
        from_attributes = True