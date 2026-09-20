from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Item(BaseModel):
    name: str

@app.get("/user/{age}")
async def path_query(age: int, message: str = None, city: str = 'Moscow'):
    return {
        "age": age,
        "message": message,
        "city": city,
    }

@app.post("/items/")
async def create_item(item: Item):
    return {
        "name": item.name
    }



