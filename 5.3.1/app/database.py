from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "5_3_1"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    count: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False, server_default='')