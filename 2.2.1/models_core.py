from sqlalchemy import Table, MetaData, Column, BigInteger, String
from pydantic import BaseModel

metadata = MetaData()

users = Table(
    "users", metadata,
    Column('id', BigInteger, primary_key=True),
    Column("username", String),
    Column("password", String),
)

class UserPost(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str