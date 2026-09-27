from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from models import users_db, UserRegister, UserLogin
import jwt
from datetime import datetime, timedelta

app = FastAPI()

SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()



def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except:
        return None


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    username = decode_token(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return username


@app.post("/register")
async def register(user: UserRegister):
    if user.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )

    hashed_password = hash_password(user.password)
    users_db[user.username] = hashed_password

    return {"message": "New user created"}


@app.post("/login")
async def login(user: UserLogin):
    if user.username not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    stored_hash = users_db[user.username]
    if not verify_password(user.password, stored_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization failed"
        )

    access_token = create_access_token(user.username)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/protected_resource")
async def protected_resource(username: str = Depends(verify_token)):
    return {
        "message": "Access granted",
        "user": username
    }
