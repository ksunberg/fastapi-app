from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from models import UserRead, User, UserPost, Base
from contextlib import asynccontextmanager

DATABASE_URL = "postgresql+psycopg://superuser:superpassword@127.0.0.1/data"
engine = create_async_engine(DATABASE_URL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan = lifespan)

async def get_db():
    async with AsyncSession(engine) as session:
        yield session

@app.post('/users', response_model=UserRead)
async def create_user(user: UserPost, db: AsyncSession = Depends(get_db)):
    new_user = User(username=user.username)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@app.get('/users/{user_id}', response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    return user


@app.get('/users/{user_id}', response_model=UserRead)
async def get_user(user_id: int):
    query = """
        SELECT id, username
        FROM users
        WHERE id = :user_id
    """
    user = await database.fetch_one(
        query=query,
        values={"user_id": user_id}
    )
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return UserRead(
        id=user["id"],
        username=user["username"]
    )