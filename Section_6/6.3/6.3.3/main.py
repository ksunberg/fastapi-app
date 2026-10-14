from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.asyncio import AsyncioIntegration
import os
import random
from models import ErrorResponse

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", ""),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    environment=os.getenv("ENVIRONMENT", "development"),
    integrations=[
        FastApiIntegration(),
        AsyncioIntegration(),
    ]
)

app = FastAPI()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    event_id = sentry_sdk.capture_exception(exc)

    sentry_sdk.set_context("request", {
        "method": request.method,
        "url": str(request.url),
        "path": request.url.path,
        "client_ip": request.client.host if request.client else None,
        "headers": dict(request.headers)
    })

    sentry_sdk.set_tag("endpoint", request.url.path)
    sentry_sdk.set_tag("method", request.method)

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Внутренняя ошибка сервера"

    return JSONResponse(
        status_code=status_code,
        content=ErrorResponse(
            status_code=status_code,
            message=message,
            event_id=event_id
        ).dict(),
        headers={"X-Error-Event-Id": event_id}
    )


@app.get("/sentry-debug")
async def sentry_debug():
    return 1 / 0


@app.get("/ok")
async def ok():
    return {"status": "ok"}


@app.get("/random-error")
async def random_error():
    errors = [
        lambda: 1 / 0,
        lambda: {}["missing"],
        lambda: int("not-a-number"),
        lambda: raise_runtime_error()
    ]
    random.choice(errors)()
    return {"status": "unreachable"}


def raise_runtime_error():
    raise RuntimeError("Случайная ошибка Runtime")


@app.get("/")
async def root():
    return {
        "message": "FastAPI с Sentry мониторингом",
        "endpoints": [
            "/ok - успешный запрос",
            "/sentry-debug - тест Sentry (ошибка)",
            "/random-error - случайная ошибка"
        ]
    }