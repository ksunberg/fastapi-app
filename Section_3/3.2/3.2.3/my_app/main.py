import os
import uuid

from fastapi import FastAPI, Form, Request, Response
from itsdangerous import SignatureExpired, TimestampSigner

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY", "my-secret-key")
signer = TimestampSigner(SECRET_KEY)

SESSION_COOKIE = "session_token"
SESSION_TTL = 300
RENEW_THRESHOLD = 180

fake_bd = {"ksu": "123"}


@app.post("/login")
async def login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
):
    if username not in fake_bd or fake_bd[username] != password:
        response.status_code = 401
        return {"message": "Invalid credentials"}
    user_id = str(uuid.uuid4())
    response.set_cookie(
        key=SESSION_COOKIE,
        value=signer.sign(user_id).decode("utf-8"),
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
        return {"message": "Invalid session"}
    try:
        user_id, _ = signer.unsign(cookie, max_age=RENEW_THRESHOLD, return_timestamp=True)
        renewed = False
    except SignatureExpired:
        try:
            user_id, _ = signer.unsign(cookie, max_age=SESSION_TTL, return_timestamp=True)
            renewed = True
        except SignatureExpired:
            response.status_code = 401
            return {"message": "Session expired"}
        except:
            response.status_code = 401
            return {"message": "Invalid session"}
    except:
        response.status_code = 401
        return {"message": "Invalid session"}

    if renewed:
        response.set_cookie(
            key=SESSION_COOKIE,
            value=signer.sign(user_id.decode("utf-8")).decode("utf-8"),
            httponly=True,
            secure=False,
            max_age=SESSION_TTL,
            path="/",
            samesite="lax",
        )

    return {"user_id": user_id.decode("utf-8"), "message": "Profile data"}
