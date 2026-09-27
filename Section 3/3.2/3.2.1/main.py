from fastapi import FastAPI, HTTPException, Request, Response
from models import UserLogin
import uuid

app = FastAPI()

sessions = {}
users_db = {}


@app.post("/login")
async def login(login_data: UserLogin, response: Response):
    session_token = str(uuid.uuid4())
    sessions[session_token] = login_data.id
    users_db[login_data.id] = login_data

    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=True
    )
    return {"message": "Login successful", "user_id": login_data.id}


@app.get("/user/{user_id}")
async def get_user(user_id: int, request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token or session_token not in sessions:
        raise HTTPException(status_code=401, detail={"message": "Unauthorized"})
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail={"message": "User not found"})
    user = users_db[user_id]
    return {
        "id": user.id,
        "username": user.username,
        "profile": "User profile info"
    }


@app.get("/user")
async def get_current_user(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token or session_token not in sessions:
        raise HTTPException(status_code=401, detail={"message": "Unauthorized"})
    user_id = sessions[session_token]
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail={"message": "User not found"})
    user = users_db[user_id]
    return {
        "id": user.id,
        "username": user.username,
        "profile": "User profile info"
    }
