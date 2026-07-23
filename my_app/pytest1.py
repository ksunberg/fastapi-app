from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

class Base(DeclarativeBase):
    pass

class UserTable(Base):
    __tablename__ = "pytest1"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

DATABASE_URL = "postgresql+psycopg://superuser:superpassword@127.0.0.1/data"
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

app = FastAPI()

async def get_db():
    async with async_session_maker() as session:
        return session


@app.post("/users/")
async def create_user(user: UserCreate):
    async with async_session_maker() as db:
        result = await db.execute(select(UserTable).where(UserTable.username == user.username))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(400, "Пользователь уже существует")
        new_user = UserTable(username=user.username, password=user.password)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return {"message": "OK", "id": new_user.id, "username": new_user.username}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    async with async_session_maker() as db:
        result = await db.execute(select(UserTable).where(UserTable.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(404, "Пользователь не найден")
        return {"id": user.id, "username": user.username}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    async with async_session_maker() as db:
        result = await db.execute(select(UserTable).where(UserTable.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(404, "Пользователь не найден")
        await db.delete(user)
        await db.commit()
        return {"message": "OK"}


@app.get("/users/")
async def get_all_users():
    async with async_session_maker() as db:
        result = await db.execute(select(UserTable))
        users = result.scalars().all()
        return [{"id": user.id, "username": user.username} for user in users]