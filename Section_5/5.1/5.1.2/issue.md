# Задача 5.1.2 — CRUD для Todo

## Описание
Интегрировать FastAPI с базой данных и реализовать CRUD-операции для ресурса «Todo».

## Задачи
1. Выбрать БД (SQLite, PostgreSQL, MySQL или MongoDB) и установить драйвер.
2. Создать модель `Todo`: `id`, `title`, `description`, `completed`.
3. `POST /todos` — создание элемента (JSON: `title`, `description`; новый элемент имеет `completed: false`), ответ 201 с созданным элементом.
4. `GET /todos/{id}` — получение элемента; если не найден — ответ об ошибке.
5. `PUT/POST /todos/{id}` — обновление полей `title`, `description`, `completed`; ответ с обновлённым элементом.
6. `DELETE /todos/{id}` — удаление; при успехе — сообщение об успехе.

## Пример
**`POST /todos`:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Ответ (201):**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false
}
```

**`GET /todos/1`** → 200 с тем же JSON.

> Материалы: [FastAPI + SQL](https://fastapi.tiangolo.com/tutorial/sql-databases/), SQL-синтаксис (W3Schools и др.).
