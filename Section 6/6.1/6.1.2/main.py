from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from loguru import logger
import random
import sys
from datetime import datetime
from models import ErrorResponse

logger.remove()

logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO"
)

logger.add(
    "logs/app_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="7 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
    level="DEBUG",
    serialize=True
)

logger.add(
    "logs/errors_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="30 days",
    level="ERROR",
    serialize=True
)

app = FastAPI()


class CustomAppError(Exception):
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code
        super().__init__(message)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    log_context = {
        "method": request.method,
        "path": request.url.path,
        "client_ip": request.client.host if request.client else None,
        "timestamp": datetime.utcnow().isoformat()
    }

    if isinstance(exc, CustomAppError):
        status_code = exc.code
        message = exc.message
        logger.bind(**log_context).error(f"Custom error: {message}")

        return JSONResponse(
            status_code=status_code,
            content={
                "status_code": status_code,
                "message": message
            }
        )

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Внутренняя ошибка сервера"

    logger.bind(**log_context).exception(f"Unhandled error: {str(exc)}")

    return JSONResponse(
        status_code=status_code,
        content={
            "status_code": status_code,
            "message": message,
            "detail": str(exc) if app.debug else None
        }
    )


@app.get("/ok")
async def ok():
    logger.info("OK endpoint called")
    return {"status": "ok"}


@app.get("/error")
async def error():
    logger.warning("Error endpoint called - raising CustomAppError")
    raise CustomAppError("Демонстрационная ошибка", code=418)


@app.get("/boom")
async def boom():
    def div_by_zero():
        return 1 / 0

    def key_err():
        return {}["missing"]

    def value_err():
        return int("not-an-int")

    def runtime_err():
        raise RuntimeError("Случайная ошибка")

    random.choice([div_by_zero, key_err, value_err, runtime_err])()
    return {"status": "unreachable"}


@app.get("/test-logging")
async def test_logging():
    logger.info("Тестовое информационное сообщение")
    logger.warning("Тестовое предупреждение")
    logger.error("Тестовое сообщение об ошибке")
    return {"message": "Логи записаны"}


@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {
        "message": "FastAPI с Loguru логированием",
        "endpoints": [
            "/ok - успешный запрос",
            "/error - вызывает CustomAppError (418)",
            "/boom - случайная ошибка (500)",
            "/test-logging - тест логирования"
        ]
    }