from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import String
from enum import Enum as PyEnum
from sqlalchemy import Enum
from sqlalchemy import Boolean, false
from sqlalchemy.types import Text

class Base(DeclarativeBase):
    pass

class ProductStatus(PyEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"

class Product(Base):
    __tablename__ = "5.3.3"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    count: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[ProductStatus] = mapped_column(
        Enum(
            ProductStatus,
            name="product_status",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
        server_default=ProductStatus.DRAFT.value,
    )
    is_featured: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=false())
