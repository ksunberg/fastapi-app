from enum import Enum as PyEnum
from sqlalchemy import Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel


class Base(DeclarativeBase):
    pass

class Product_Response(BaseModel):
    title: str
    price: float
    count: int


class Product(Base):
    __tablename__ = "5_3_2"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    count: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False, server_default='')
