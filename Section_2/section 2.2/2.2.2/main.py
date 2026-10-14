from fastapi import FastAPI
from models import User

app = FastAPI()

@app.post('/user')
async def is_adult(user:User):
    return {
        "name": user.username,
        "age": user.age,
        "is_adult": user.age
    }

#добавить сложное условие проверки возраста, не меньше 18 не больше 60 не равно 35 и сумма цифр нечетная, реализуй это все в модели пидантик