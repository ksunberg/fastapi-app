from fastapi import FastAPI, Header
from models import CommonHeaders, MINIMUM_APP_VERSION
from datetime import datetime

app = FastAPI()

@app.get("/headers")
async def get_headers(headers: CommonHeaders = Header(...)):
    return {
        "User-Agent": headers.user_agent,
        "Accept-Language": headers.accept_language
    }

@app.get("/info")
async def get_info(headers: CommonHeaders = Header(...)):
    from fastapi.responses import JSONResponse
    response = JSONResponse({
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": {
            "User-Agent": headers.user_agent,
            "Accept-Language": headers.accept_language
        }
    })
    response.headers["X-Server-Time"] = datetime.now().isoformat()
    return response