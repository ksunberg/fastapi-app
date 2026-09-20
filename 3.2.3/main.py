from fastapi import FastAPI, Request, Form, Response
from itsdangerous import Signer
import uuid
import time

app = FastAPI()

SECRET_KEY = "my-secret-key"
signer = Signer(SECRET_KEY)

FAKE_DB = {
    "ksu": "123"
}


def create_cookie(user_id, timestamp):
    data = f"{user_id}.{timestamp}"
    return signer.sign(data).decode('utf-8')


def verify_cookie(cookie_value):
    try:
        data = signer.unsign(cookie_value).decode('utf-8')
        user_id, timestamp = data.split('.')
        return user_id, int(timestamp)
    except:
        return None, None


@app.post("/login")
async def login(response: Response, username: str = Form(...), password: str = Form(...)):
    if username not in FAKE_DB or FAKE_DB[username] != password:
        response.status_code = 401
        return {"message": "Invalid credentials"}
    user_id = str(uuid.uuid4())
    timestamp = int(time.time())
    cookie_value = create_cookie(user_id, timestamp)
    response.set_cookie(
        key="session_token",
        value=cookie_value,
        httponly=True,
        max_age=300
    )
    return {"message": "Login successful"}


@app.get("/profile")
async def profile(request: Request, response: Response):
    cookie = request.cookies.get("session_token")
    if not cookie:
        response.status_code = 401
        return {"message": "Unauthorized"}
    user_id, timestamp = verify_cookie(cookie)
    if not user_id:
        response.status_code = 401
        return {"message": "Invalid session"}
    current_time = int(time.time())
    elapsed = current_time - timestamp
    if elapsed > 300:
        response.status_code = 401
        return {"message": "Session expired"}
    if elapsed >= 180:
        new_timestamp = current_time
        new_cookie = create_cookie(user_id, new_timestamp)
        response.set_cookie(
            key="session_token",
            value=new_cookie,
            httponly=True,
            max_age=300
        )
    return {"user_id": user_id, "message": "Profile data"}
