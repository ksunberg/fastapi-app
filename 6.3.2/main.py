from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import time
from models import ErrorResponse, UserCreate, UserResponse

app = FastAPI()

users = {}
user_id = 1


class UserNotFoundError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


@app.exception_handler(UserNotFoundError)
async def handle_not_found(request: Request, exc: UserNotFoundError):
    start = time.time()

    response = JSONResponse(
        status_code=404,
        content=ErrorResponse(
            status_code=404,
            message="Пользователь не найден",
            error_code="USER_NOT_FOUND"
        ).dict()
    )

    response.headers["X-ErrorHandleTime"] = f"{(time.time() - start) * 1000:.2f}ms"
    return response


@app.exception_handler(UserAlreadyExistsError)
async def handle_already_exists(request: Request, exc: UserAlreadyExistsError):
    start = time.time()

    response = JSONResponse(
        status_code=409,
        content=ErrorResponse(
            status_code=409,
            message="Пользователь уже существует",
            error_code="USER_ALREADY_EXISTS"
        ).dict()
    )

    response.headers["X-ErrorHandleTime"] = f"{(time.time() - start) * 1000:.2f}ms"
    return response


@app.exception_handler(HTTPException)
async def handle_http_error(request: Request, exc: HTTPException):
    start = time.time()

    response = JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status_code=exc.status_code,
            message=exc.detail,
            error_code="HTTP_ERROR"
        ).dict()
    )

    response.headers["X-ErrorHandleTime"] = f"{(time.time() - start) * 1000:.2f}ms"
    return response


@app.exception_handler(Exception)
async def handle_all_errors(request: Request, exc: Exception):
    start = time.time()

    response = JSONResponse(
        status_code=500,
        content=ErrorResponse(
            status_code=500,
            message="Внутренняя ошибка сервера",
            error_code="INTERNAL_ERROR"
        ).dict()
    )

    response.headers["X-ErrorHandleTime"] = f"{(time.time() - start) * 1000:.2f}ms"
    return response


@app.post("/users")
async def create_user(user: UserCreate):
    for u in users.values():
        if u["username"] == user.username:
            raise UserAlreadyExistsError()

    global user_id
    users[user_id] = {
        "id": user_id,
        "username": user.username,
        "email": user.email,
        "password": user.password
    }
    user_id += 1

    return {"message": "Пользователь создан", "user_id": user_id - 1}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id not in users:
        raise UserNotFoundError()

    user = users[user_id]
    return UserResponse(
        id=user["id"],
        username=user["username"],
        email=user["email"]
    )


@app.get("/users")
async def get_all_users():
    return list(users.values())


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    if user_id not in users:
        raise UserNotFoundError()

    del users[user_id]
    return {"message": "Пользователь удален"}


@app.get("/")
async def root():
    return {"message": "API с обработкой ошибок"}