from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from typing import Optional, List

from models import (
    UserCreate, UserResponse,
    TodoCreate, TodoUpdate, TodoResponse
)

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/todo_db"
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    todos = relationship("Todo", back_populates="user", cascade="all, delete-orphan")


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="todos")


app = FastAPI()


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(
        (User.username == user.username) | (User.email == user.email)
    )
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким username или email уже существует"
        )

    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=user.password_hash
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@app.get("/users/", response_model=List[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    stmt = select(User)
    result = await db.execute(stmt)
    users = result.scalars().all()
    return users


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    await db.delete(user)
    await db.commit()

    return {"message": "User and associated todos deleted"}


@app.post("/todos/", response_model=TodoResponse)
async def create_todo(todo: TodoCreate, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.id == todo.user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        user_id=todo.user_id
    )
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo


@app.get("/todos/", response_model=List[TodoResponse])
async def get_todos(
        user_id: Optional[int] = None,
        db: AsyncSession = Depends(get_db)
):
    stmt = select(Todo)
    if user_id:
        stmt = stmt.where(Todo.user_id == user_id)

    result = await db.execute(stmt)
    todos = result.scalars().all()
    return todos


@app.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Todo).where(Todo.id == todo_id)
    result = await db.execute(stmt)
    todo = result.scalar_one_or_none()

    if not todo:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return todo


@app.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(
        todo_id: int,
        todo_update: TodoUpdate,
        db: AsyncSession = Depends(get_db)
):
    stmt = select(Todo).where(Todo.id == todo_id)
    result = await db.execute(stmt)
    todo = result.scalar_one_or_none()

    if not todo:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    if todo_update.title is not None:
        todo.title = todo_update.title
    if todo_update.description is not None:
        todo.description = todo_update.description
    if todo_update.completed is not None:
        todo.completed = todo_update.completed
    if todo_update.user_id is not None:
        user_stmt = select(User).where(User.id == todo_update.user_id)
        user_result = await db.execute(user_stmt)
        user = user_result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        todo.user_id = todo_update.user_id

    await db.commit()
    await db.refresh(todo)
    return todo


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Todo).where(Todo.id == todo_id)
    result = await db.execute(stmt)
    todo = result.scalar_one_or_none()

    if not todo:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    await db.delete(todo)
    await db.commit()

    return {"message": "Todo deleted"}


@app.get("/")
async def root():
    return {
        "message": "Todo API с интеграцией Users (асинхронный)",
        "endpoints": [
            "/users/ (POST, GET)",
            "/users/{id} (GET, DELETE)",
            "/todos/ (POST, GET)",
            "/todos/{id} (GET, PUT, DELETE)"
        ]
    }


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)