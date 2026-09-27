# Задача 3.2.1 — Аутентификация через cookie

## Описание
Реализовать аутентификацию на основе файлов cookie.

## Задачи
1. Создать маршрут `POST /login`, принимающий имя пользователя и пароль (данные формы/JSON). При успешной проверке установить безопасный HTTP-only cookie `session_token` с уникальным значением (например, UUID).
2. Реализовать защищённый маршрут `GET /user`, требующий cookie `session_token`. При действительном cookie вернуть JSON с профилем пользователя.
3. При отсутствии или недействительности cookie вернуть ошибку 401 или `{"message": "Unauthorized"}`.

## Пример
**Логин:**
```json
{
  "username": "user123",
  "password": "password123"
}
```
Ответ должен содержать cookie `session_token`.

**Доступ к `/user`:**
- С cookie `session_token: "abc123xyz456"` → информация профиля.
- Без cookie или с `session_token: "invalid_token_value"` → ошибка 401 / `{"message": "Unauthorized"}`.

> Протестируйте через curl, Postman или любой другой API-клиент.
