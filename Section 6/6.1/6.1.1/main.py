from fastapi import FastAPI
from fastapi.responses import JSONResponse
from httpx import Request

from models import CustomExceptionA, CustomExceptionB, ErrorResponse

app = FastAPI()

@app.exception_handler(CustomExceptionA)
async def exception_a(reques: Request, exc: CustomExceptionA):
    print(f"Ошибка A: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error="CustomExceptionA",
            message=exc.message,
            status_code=exc.status_code
        ).dict()
    )

@app.exception_handler(CustomExceptionB)
async def exception_b(reques: Request, exc: CustomExceptionB):
    print(f"Ошибка B: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error="CustomExceptionB",
            message=exc.message,
            status_code=exc.status_code
        ).dict()
    )

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id < 0:
        raise CustomExceptionA("ID не может быть отрицательным")
    items = {1: "item1", 2: "item2", 3: "item3"}
    if item_id not in items:
        raise CustomExceptionB(f"Товар с ID {item_id} не найден")
    return {"item_id": item_id, "name": items[item_id]}


@app.get("/user/{user_id}")
async def get_user(user_id: int):
    if user_id == 0:
        raise CustomExceptionA("ID пользователя не может быть 0")
    users = {1: "ksu", 2: "kot", 3: "kotik"}
    if user_id not in users:
        raise CustomExceptionB(f"Пользователь с ID {user_id} не найден")
    return {"user_id": user_id, "name": users[user_id]}
