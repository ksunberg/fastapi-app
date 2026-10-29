import os
import uuid

from fastapi import FastAPI, Form, Request, status
from fastapi.responses import JSONResponse
from itsdangerous import BadSignature, BadTimeSignature, SignatureExpired, Signer

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY", "my-secret-key-for-signing")
signer = Signer(SECRET_KEY)

fake_db = {
    "alice": "password123",
    "bob": "qwerty",
}

user_ids = {username: str(uuid.uuid4()) for username in fake_db}


@app.post("/login")
async def login(
        username: str = Form(..., description="Имя пользователя"),
        password: str = Form(..., description="Пароль")
):
    if username not in fake_db or fake_db[username] != password:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Invalid credentials"}
        )
    user_id = user_ids[username]
    signed_value = signer.sign(user_id).decode('utf-8')
    response = JSONResponse({"message": "Login successful", "user_id": user_id})
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
    except SignatureExpired:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Session expired"}
        )
    except BadTimeSignature:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Unauthorized"}
        )
    except BadSignature:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Unauthorized"}
        )
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Unauthorized"}
        )
    username = next(
        (name for name, uid in user_ids.items() if uid == user_id),
        None
    )
    if username is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Unauthorized"}
        )
    return {
        "user_id": user_id,
        "username": username,
        "message": "Profile data",
        "status": "authenticated"
    }
