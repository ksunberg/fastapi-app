# Задача 7.1.1 — Асинхронные тесты (pytest-asyncio + httpx)

## Описание
Написать асинхронные модульные тесты для FastAPI-приложения с тремя эндпоинтами и in-memory хранилищем. Использовать `pytest-asyncio`, `httpx.AsyncClient` (через `ASGITransport`) и `Faker`.

## Стартовый код
```python
# my_project/main.py
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from itertools import count
from threading import Lock

app = FastAPI()
db: dict[int, dict] = {}
_id_seq = count(start=1)
_id_lock = Lock()

def next_user_id() -> int:
    with _id_lock:
        return next(_id_seq)

class UserIn(BaseModel):
    username: str
    age: int

class UserOut(BaseModel):
    id: int
    username: str
    age: int

@app.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserIn):
    user_id = next_user_id()
    db[user_id] = user.model_dump()
    return {"id": user_id, **db[user_id]}

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id, **db[user_id]}

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    if db.pop(user_id, None) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=204)
```

## Задачи
1. **Окружение:** установить `pytest`, `pytest-asyncio`, `httpx`, `Faker`; создать папку `tests/`.
2. **Асинхронные тесты** для всех трёх эндпоинтов:
   - создание пользователя (201) и валидация структуры ответа;
   - получение существующего (200);
   - получение несуществующего (404);
   - удаление существующего (204);
   - повторное удаление (404).
3. **HTTP-клиент без сервера:** использовать `httpx.AsyncClient` с `ASGITransport` (без запуска Uvicorn).
4. **Данные через Faker:** генерировать username, возраст и проверять валидные и граничные значения.
5. **Изоляция состояния:** очищать in-memory словарь до/после каждого теста; при желании сгруппировать кейсы в класс.
6. **Запуск:** `pytest` — все тесты должны проходить.

## Критерии приёмки
- Тесты асинхронные, выполняются через `httpx.AsyncClient` + `ASGITransport`.
- Используется Faker для генерации входных данных.
- Покрыты успешные и ошибочные сценарии всех трёх эндпоинтов.
- Состояние хранилища изолировано между тестами.

> Материалы: [FastAPI async-тесты](https://fastapi.tiangolo.com/advanced/async-tests/), [pytest-asyncio](https://pytest-asyncio.readthedocs.io/), [HTTPX Async Support](https://www.python-httpx.org/async/).
