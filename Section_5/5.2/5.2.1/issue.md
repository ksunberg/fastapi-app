# Задача 5.2.1 — Асинхронный CRUD

## Описание
Второй шанс выполнить задачу повышенной сложности из предыдущего урока — теперь с асинхронностью.

## Задачи
Взять CRUD-приложение Todo (см. задачу 5.1.2) и сделать его **асинхронным**:

1. Выбрать БД (например, SQLite/PostgreSQL/MySQL/MongoDB) и установить драйвер.
2. Создать модель `Todo`: `id`, `title`, `description`, `completed`.
3. `POST /todos` — создание элемента (JSON: `title`, `description`; `completed: false` по умолчанию), ответ 201.
4. `GET /todos/{id}` — получение элемента или ответ об ошибке, если не найден.
5. `PUT/POST /todos/{id}` — обновление полей `title`, `description`, `completed`.
6. `DELETE /todos/{id}` — удаление с сообщением об успехе.

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
