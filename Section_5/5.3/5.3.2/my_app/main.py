import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from my_app.database import Product
from my_app.models import ProductResponse

load_dotenv()

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db():
    async with async_session_maker() as session:
        yield session


@app.post("/product/")
async def create_product(product: ProductResponse, db: AsyncSession = Depends(get_db)):
    db_product = Product(
        title=product.title,
        price=product.price,
        count=product.count,
        description=product.description,
    )
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product