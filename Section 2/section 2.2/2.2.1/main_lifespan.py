from fastapi import FastAPI, HTTPException
from models_core import UserRead, UserPost, users
from contextlib import asynccontextmanager
from databases import Database

DATABASE_URL = "postgresql+psycopg2://superuser:superpassword@127.0.0.1/postgres"
database = Database(DATABASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


@app.post('/users')
async def create_user(user: UserPost):
    query = """
        INSERT INTO users (username, password)
        VALUES (:username, :password) 
        
    """
    try:
        await database.execute(
            query=query,
            values=user.model_dump()
        )
        return {"message": "Пользователь создан"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при создании пользователя: {str(e)}"
        )





