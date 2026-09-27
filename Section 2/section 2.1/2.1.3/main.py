from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DATABASE_URL = "postgresql+psycopg://superuser:superpassword@127.0.0.1/data"
engine = create_async_engine(DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db():
    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    pass


class Calculation(Base):
    __tablename__ = "calculator"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    num1: Mapped[int]
    num2: Mapped[int]
    result: Mapped[int]


app = FastAPI()



@app.get('/calculate/{num1}/{num2}')
async def calculate(num1: int, num2: int, db: AsyncSession = Depends(get_db)):
    result = num1 + num2
    calculation = Calculation(num1=num1, num2=num2, result=result)
    db.add(calculation)
    await db.commit()
    await db.refresh(calculation)
    return {"request_id": calculation.id, "result": result}