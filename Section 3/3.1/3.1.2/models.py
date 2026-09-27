from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from pydantic import BaseModel

class Base(DeclarativeBase):
    pass

class Table(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    categorya: Mapped[str]
    price: Mapped[int] = mapped_column(nullable=True)

class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float

