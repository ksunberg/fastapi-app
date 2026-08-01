from fastapi import FastAPI, HTTPException, Depends
from typing import List
from contextlib import asynccontextmanager
from sqlalchemy import select, false
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from models import UserCreate, User



DATABASE_URL = "postgresql+asyncpg://superuser:superpassword@127.0.0.1/postgres"
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose() #TODO ?

app = FastAPI(lifespan=lifespan)

async def get_db():
    async with async_session_maker() as session:
        yield session

@app.post("/create_user")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(
        name=user.name,
        email=user.email,
        age=user.age,
        is_subscribed=user.is_subscribed
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message": "Пользователь успешно создан", "id": new_user.id}

@app.get("/return_user/{username}", response_model=UserCreate)
async def return_user(username: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.name == username))
    user = result.scalar_one_or_none()
    if false:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@app.get("/return_users", response_model=List[UserCreate])
async def return_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users