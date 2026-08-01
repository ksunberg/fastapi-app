from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from models import CommonHeaders
from datetime import datetime

app = FastAPI()


@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Ошибка валидации заголовков",
            "message": str(exc)
        }
    )


@app.get("/headers")
async def get_headers(headers: CommonHeaders):
    return {
        "User-Agent": headers.user_agent,
        "Accept-Language": headers.accept_language
    }


@app.get("/info")
async def get_info(headers: CommonHeaders):
    response = JSONResponse(
        content={
            "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
            "headers": {
                "User-Agent": headers.user_agent,
                "Accept-Language": headers.accept_language
            }
        }
    )
    current_time = datetime.now().isoformat()
    response.headers["X-Server-Time"] = current_time
    return response
