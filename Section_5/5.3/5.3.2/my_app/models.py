from pydantic import BaseModel

class ProductResponse(BaseModel):
    title: str
    price: float
    count: int
    description: str
