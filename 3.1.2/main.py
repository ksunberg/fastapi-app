from fastapi import FastAPI, HTTPException, Depends
from models import Product, Table, Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select

DATABASE_URL = "postgresql+psycopg://superuser:superpassword@127.0.0.1:5432/postgres"

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

app = FastAPI()


async def get_db():
    async with async_session_maker() as session:
        yield session


@app.post("/post_products")
async def post_products(product: Product, db: AsyncSession = Depends(get_db)):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db_product = Table(
        name=product.name,
        categorya=product.category,
        price=product.price
    )
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


@app.get("/product/{product_id}")
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    result = await db.execute(select(Table).where(Table.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(404, "Product not found")
    return product
