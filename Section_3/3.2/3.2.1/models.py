from pydantic import BaseModel

class UserLogin(BaseModel):
    id: int
    username: str
    password: str