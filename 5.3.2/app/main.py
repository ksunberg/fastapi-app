from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from models import ProductStatus, Product, Product_Response



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
        count=product.count,
    )
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product
