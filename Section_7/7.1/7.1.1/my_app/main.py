from fastapi import FastAPI, HTTPException, Depends
from .models import UserCreate, UserResponse, UserTable
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
from typing import List


DATABASE_URL = "postgresql+psycopg://superuser:superpassword@127.0.0.1/postgres"
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

app = FastAPI()

async def get_db():
    async with async_session_maker() as session:
        return session

@app.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = UserTable(
        username = user.username,
        password = user.password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return {"massage": "Пользователь создан"}

@app.get("/user_info/{user_id}")
async def user_info(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserTable).where(UserTable.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "Пользователь не найден")
    return {"id": user.id, "username": user.username}


@app.get("/all_user_info", response_model=List[UserResponse])
async def get_all_info(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserTable))
    users = result.scalars().all()
    return users


