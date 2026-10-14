import os
import time
import uuid

from fastapi import FastAPI, Form, Request, Response
from itsdangerous import BadSignature, Signer

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY", "my-secret-key")
signer = Signer(SECRET_KEY)

SESSION_COOKIE = "session_token"
SESSION_TTL = 300
RENEW_THRESHOLD = 180

FAKE_DB = {"ksu": "123"}


def create_cookie(user_id: str, timestamp: int) -> str:
    data = f"{user_id}.{timestamp}"
    return signer.sign(data).decode("utf-8")


def verify_cookie(cookie_value: str) -> tuple[str | None, int | None]:
    try:
        data = signer.unsign(cookie_value).decode("utf-8")
    except BadSignature:
        return None, None
    try:
        user_id, timestamp = data.split(".")
        return user_id, int(timestamp)
    except ValueError:
        return None, None


@app.post("/login")
async def login(response: Response,
                username: str = Form(...),
                password: str = Form(...),):
    if username not in FAKE_DB or FAKE_DB[username] != password:
        response.status_code = 401
        return {"message": "Invalid credentials"}

    user_id = str(uuid.uuid4())
    timestamp = int(time.time())
    cookie_value = create_cookie(user_id, timestamp)
    response.set_cookie(
        key=SESSION_COOKIE,
        value=cookie_value,
        httponly=True,
        secure=False,
        max_age=SESSION_TTL,
        path="/",
        samesite="lax",
    )
    return {"message": "Login successful"}


@app.get("/profile")
async def profile(request: Request, response: Response):
    cookie = request.cookies.get(SESSION_COOKIE)
    if not cookie:
        response.status_code = 401
        return {"message": "Session expired"}

    user_id, timestamp = verify_cookie(cookie)
    if not user_id or not timestamp:
        response.status_code = 401
        return {"message": "Invalid session"}

    current_time = int(time.time())
    elapsed = current_time - timestamp
    if elapsed < 0 or elapsed > SESSION_TTL:
        response.status_code = 401
        return {"message": "Session expired"}

    if elapsed >= RENEW_THRESHOLD:
        new_cookie = create_cookie(user_id, current_time)
        response.set_cookie(
            key=SESSION_COOKIE,
            value=new_cookie,
            httponly=True,
            secure=False,
            max_age=SESSION_TTL,
            path="/",
            samesite="lax",
        )

    return {"user_id": user_id, "message": "Profile data"}
