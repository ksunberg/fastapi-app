# Задача 4.2.2 — JWT + регистрация + rate limiting

## Описание
Расширить JWT-решение: добавить регистрацию, безопасную проверку паролей и ограничение частоты запросов.

## Задачи
1. **`POST /register`:**
   - JSON: `username` (str), `password` (str).
   - Если пользователь уже существует → 409 `{"detail": "User already exists"}`.
   - Иначе сохранить пользователя с хешем пароля (PassLib/bcrypt) → 201 `{"message": "New user created"}`.

2. **`POST /login`:**
   - Пользователь не найден → 404 `{"detail": "User not found"}`.
   - Сравнивать `username` через `secrets.compare_digest()` (защита от тайминг-атак).
   - Пароль верен → JWT-токен с полезной нагрузкой `{"sub": username}`.
   - Пароль неверен → 401 `{"detail": "Authorization failed"}`.

3. **Rate limiter:**
   - `/register`: 1 запрос/минуту.
   - `/login`: 5 запросов/минуту.
   - При превышении → 429 `{"detail": "Too many requests"}`.
   - Можно использовать `slowapi` или `fastapi-limiter`.

## Примеры
**Регистрация:**
```json
{ "username": "alice", "password": "qwerty123" }
```
Ответы: 201 `{"message": "New user created"}` / 409 `{"detail": "User already exists"}`.

**Логин:**
```json
{ "username": "alice", "password": "qwerty123" }
```
Ответы: 200 `{"access_token": "eyJhbGci...", "token_type": "bearer"}` / 404 / 401.

**Protected Resource:**
```
GET /protected_resource
Authorization: Bearer eyJhbGci...
```
Ответ: 200 `{"message": "Access granted"}`.

> Требования: PassLib (bcrypt), `secrets.compare_digest()`, хранилище в памяти. Используйте параметризованные запросы и HTTPS в реальных проектах.
