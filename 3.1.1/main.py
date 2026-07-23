from fastapi import FastAPI, HTTPException
from models import Table, UserCreate
from databases import Database
from contextlib import asynccontextmanager
from databases.interfaces import Record
from typing import List

DATABASE_URL = "postgresql://superuser:superpassword@127.0.0.1/postgres"

database = Database(DATABASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)


@app.post("/create_user")
async def create_user(user: UserCreate):
    query = """
        INSERT INTO userss (name, email, age, is_subscribed) 
        VALUES (:name, :email, :age, :is_subscribed) 
        RETURNING id
    """
    try:
        await database.execute(query=query, values=user.model_dump())
        return {"message": "рукажопа"}
    except Exception as e:
        print(f"Ошибка: {e}")
        raise HTTPException(400, f"Ошибка: {str(e)}")

def record_to_dict(record: Record) -> dict:
    return {i: record[i] for i in record}

@app.get("/return_user", response_model=UserCreate)
async def return_user():
    query = "SELECT * FROM userss"
    try:
        user = await database.fetch_one(query)
        return UserCreate(**record_to_dict(user))
    except Exception as e:
        print(f"Ошибка при чтении: {e}")
        raise HTTPException(400, f"Ошибка: {str(e)}")

@app.get("/return_users", response_model=List[UserCreate])
async def return_user():
    sp = []
    query = "SELECT * FROM userss"
    try:
        return [UserCreate(**record_to_dict(k)) for k in await database.fetch_all(query)]
    except Exception as e:
        print(f"Ошибка при чтении: {e}")
        raise HTTPException(400, f"Ошибка: {str(e)}")