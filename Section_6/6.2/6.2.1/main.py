from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field, conint, constr
from typing import Optional

app = FastAPI()

class User(BaseModel):
    username: str
    age: conint(gt=18)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = 'Unknown'

@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Ошибка валидации",
            "message": str(exc)
        }
    )

@app.post("/users/")
async def create_user(user: User):
    return {
        "message": "Пользователь успешно создан",
        "user": user.dict()
    }
