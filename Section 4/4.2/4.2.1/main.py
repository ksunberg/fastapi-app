from fastapi import FastAPI, Depends
from security import create_jwt_token, get_user_from_token
from models import User

app = FastAPI()

USERS_DATA = [
    {"username": "admin", "password": "adminpass"}
]

def get_user(username: str):
    for user in USERS_DATA:
        if user.get("username") == username:
            return user
    return None

@app.post("/login")
async def login(user_in: User):
    for user in USERS_DATA:
        if user.get("username") == user_in.username and user.get("password") == user_in.password:
            token = create_jwt_token({"sub": user_in.username})
            return {"access_token": token, "token_type": "bearer"}
    return {"error": "Invalid credentials"}

@app.get("/about_me")
async def about_me(current_user: str = Depends(get_user_from_token)):
    user = get_user(current_user)
    if user:
        return user
    return {"error": "User not found"}
