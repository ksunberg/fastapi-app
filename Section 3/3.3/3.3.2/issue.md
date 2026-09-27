# Задача 3.3.2 — Модель CommonHeaders

## Описание
Оптимизировать работу с заголовками: вынести их в переиспользуемую Pydantic-модель (принцип DRY) и использовать в двух маршрутах.

## Задачи
1. **Модель `CommonHeaders`:**
   - `User-Agent` — обязательное поле;
   - `Accept-Language` — обязательное поле;
   - *(необязательно)* валидация формата `Accept-Language`.

2. **Маршрут `GET /headers`:**
   - внедрить модель `CommonHeaders`;
   - вернуть JSON со значениями `User-Agent` и `Accept-Language`.

3. **Маршрут `GET /info`:**
   - аналогично получить заголовки через модель;
   - вернуть JSON: `{"message": "Добро пожаловать! Ваши заголовки успешно обработаны.", "headers": {...}}`;
   - добавить HTTP-заголовок ответа `X-Server-Time` с текущим серверным временем.

## Примеры
**`GET /headers`** → 
```json
{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9,es;q=0.8"
}
```

**`GET /info`** →
```json
{
    "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9,es;q=0.8"
    }
}
```
Плюс заголовок `X-Server-Time: 2025-04-16T12:34:56`.

> Материалы: FastAPI — [Header Parameters and Models](https://fastapi.tiangolo.com/tutorial/header-params/).
