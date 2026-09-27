from pydantic import BaseModel, field_validator, Field
from fastapi import HTTPException

class User(BaseModel):
    username: str
    age: int
    @field_validator("age")
    @classmethod
    def validate_age(cls, age: int):
        if age < 18:
            raise HTTPException(status_code=400, detail="Возраст должен быть не меньше 18")
        if age > 60:
            raise HTTPException(status_code=400, detail="Возраст должен быть не больше 60")
        if age == 35:
            raise HTTPException(status_code=400, detail="Возраст не должен быть равен 35")
        a = 0
        for k in str(age):
            a += int(k)
        if a % 2 == 0:
            raise HTTPException(status_code=400, detail="Сумма цифр возраста должна быть нечетной")
        return age
