from fastapi import FastAPI, HTTPException, Request, Form, status
from fastapi.responses import JSONResponse
from itsdangerous import Signer, BadSignature
import uuid
import os

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY", "my-secret-key-for-signing")
signer = Signer(SECRET_KEY)

FAKE_DB = {
    "alice": "password123",
    "bob": "qwerty",
}


@app.post("/login")
async def login(
        username: str = Form(..., description="Имя пользователя"),
        password: str = Form(..., description="Пароль")
):
    if username not in FAKE_DB or FAKE_DB[username] != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    user_id = str(uuid.uuid4())
    signed_value = signer.sign(user_id).decode('utf-8')
    response = JSONResponse({"message": "Вход успешен", "user_id": user_id})
    response.set_cookie(
        key="session_token",
        value=signed_value,
        httponly=True,
        max_age=3600,
        path="/"
    )
    return response


@app.get("/profile")
async def profile(request: Request):
    session_token = request.cookies.get("session_token")

    if not session_token:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Unauthorized"}
        )
    try:
        user_id = signer.unsign(session_token).decode('utf-8')
    except BadSignature:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Unauthorized"}
        )
    return {
        "user_id": user_id,
        "message": "Profile data",
        "status": "authenticated"
    }

