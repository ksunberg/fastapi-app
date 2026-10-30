import os
import time
import uuid

from fastapi import FastAPI, Form, Request, Response
from itsdangerous import TimestampSigner

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY", "my-secret-key")
signer = TimestampSigner(SECRET_KEY)

SESSION_COOKIE = "session_token"
SESSION_TTL = 300
RENEW_THRESHOLD = 180

FAKE_DB = {"ksu": "123"}


def create_cookie(user_id: str) -> str:
    return signer.sign(user_id).decode("utf-8")


def verify_cookie(cookie_value: str | None) -> tuple[str, int] | None:
    if not cookie_value:
        return None
    try:
        user_id, signed_at = signer.unsign(
            cookie_value,
            max_age=SESSION_TTL,
            return_timestamp=True,
        )
        return user_id.decode("utf-8"), int(signed_at.timestamp())
    except:
        return None


@app.post("/login")
async def login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
):
    if username not in FAKE_DB or FAKE_DB[username] != password:
        response.status_code = 401
        return {"message": "Invalid credentials"}
    user_id = str(uuid.uuid4())
    response.set_cookie(
        key=SESSION_COOKIE,
        value=create_cookie(user_id),
        httponly=True,
        secure=False,
        max_age=SESSION_TTL,
        path="/",
        samesite="lax",
    )
    return {"message": "Login successful"}


@app.get("/profile")
async def profile(request: Request, response: Response):
    result = verify_cookie(request.cookies.get(SESSION_COOKIE))
    if result is None:
        response.status_code = 401
        return {"message": "Invalid session"}
    user_id, signed_at = result
    age = int(time.time()) - signed_at
    if age >= RENEW_THRESHOLD:
        response.set_cookie(
            key=SESSION_COOKIE,
            value=create_cookie(user_id),
            httponly=True,
            secure=False,
            max_age=SESSION_TTL,
            path="/",
            samesite="lax",
        )

    return {"user_id": user_id, "message": "Profile data"}