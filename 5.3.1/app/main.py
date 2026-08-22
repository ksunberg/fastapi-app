from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "5_3_1"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    count: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False, server_default='')

class Product_Response(BaseModel):
    title: str
    price: float
    count: int

app = FastAPI()

DATABASE_URL = "postgresql+psycopg://superuser:superpassword@127.0.0.1/postgres"
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with async_session_maker() as session:
        yield session

@app.post("/product/")
async def create_product(product: Product_Response, db: AsyncSession = Depends(get_db)):
    db_product = Product(
        title=product.title,
        price=product.price,
        count=product.count
    )
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


