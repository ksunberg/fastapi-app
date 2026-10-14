from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
from models import User, UserTable
app = FastAPI()
DATABASE_URL = "postgresql+psycopg://superuser:superpassword@127.0.0.1/postgres"
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with async_session_maker() as session:
        yield session

@app.post("/reg")
async def reg_user(user: User, db: AsyncSession = Depends(get_db)):
    db_user = UserTable(
        username=user.username,
        password=user.password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return {"message": "Пользователь создан"}

@app.get("/info/{user_id}")
async def info_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserTable).where(UserTable.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "Пользователь не найден")
    return {"id": user.id, "username": user.username}