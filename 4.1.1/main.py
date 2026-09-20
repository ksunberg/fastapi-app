from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
from models import UserLogin, UserTable, UserRegister

app = FastAPI()
security = HTTPBasic()

DATABASE_URL = "postgresql+psycopg://superuser:superpassword@127.0.0.1/postgres"
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db():
    async with async_session_maker() as session:
        yield session

@app.post("/register")
async def register(user: UserRegister, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserTable).where(UserTable.username == user.username))
    sush_user = result.scalar_one_or_none()
    if sush_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь уже существует"
        )
    new_user = UserTable(username=user.username, password=user.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message": f"Пользователь {user.username} успешно зарегистрирован"}

async def authenticate(credentials: HTTPBasicCredentials = Depends(security),
                       db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserTable).where(UserTable.username == credentials.username))
    user = result.scalar_one_or_none()
    if not user or user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The credentials are incorrect",
            headers={"WWW-Authenticate": "Basic"}
        )
    return UserLogin(username=user.username, password=user.password)

@app.get("/login")
async def login(user: UserLogin = Depends(authenticate)):
    return {"message": "You got my secret, welcome"}
