from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time
from models import UserNotFoundException, UserExistsException, InvalidUserDataException, users_db, ErrorResponseModel

app = FastAPI()


@app.exception_handler(UserNotFoundException)
async def handle_user_not_found(request: Request, exc: UserNotFoundException):
    response = JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponseModel(
            status_code=exc.status_code,
            message=exc.message,
            error_code=exc.error_code
        ).dict()
    )
    response.headers["X-ErrorHandleTime"] = f"{time.time():.4f}"
    return response


@app.exception_handler(InvalidUserDataException)
async def handle_invalid_user_data(request: Request, exc: InvalidUserDataException):
    response = JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponseModel(
            status_code=exc.status_code,
            message=exc.message,
            error_code=exc.error_code
        ).dict()
    )
    response.headers["X-ErrorHandleTime"] = f"{time.time():.4f}"
    return response


@app.exception_handler(UserExistsException)
async def handle_user_exists(request: Request, exc: UserExistsException):
    response = JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponseModel(
            status_code=exc.status_code,
            message=exc.message,
            error_code=exc.error_code
        ).dict()
    )
    response.headers["X-ErrorHandleTime"] = f"{time.time():.4f}"
    return response


@app.post("/register")
async def register_user(username: str, password: str):
    if not username or len(username) < 3:
        raise InvalidUserDataException("Имя пользователя должно содержать минимум 3 символа")

    if not password or len(password) < 6:
        raise InvalidUserDataException("Пароль должен содержать минимум 6 символов")

    if username in users_db:
        raise UserExistsException(f"Пользователь '{username}' уже существует")

    users_db[username] = {"username": username, "password": password}
    return {"message": "Пользователь успешно зарегистрирован", "username": username}


@app.get("/users/{username}")
async def get_user(username: str):
    if username not in users_db:
        raise UserNotFoundException(f"Пользователь '{username}' не найден")

    return {
        "username": users_db[username]["username"],
        "message": "Пользователь найден"
    }
