from datetime import datetime

from fastapi import FastAPI, Header, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from models import CommonHeaders

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Ошибка валидации заголовков",
            "message": str(exc),
        },
    )


@app.get("/headers")
async def get_headers(headers: CommonHeaders = Header(...)):
    return {
        "User-Agent": headers.user_agent,
        "Accept-Language": headers.accept_language,
    }


@app.get("/info")
async def get_info(headers: CommonHeaders = Header(...)):
    response = JSONResponse(
        content={
            "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
            "headers": {
                "User-Agent": headers.user_agent,
                "Accept-Language": headers.accept_language,
            },
        }
    )
    response.headers["X-Server-Time"] = datetime.now().isoformat()
    return response
