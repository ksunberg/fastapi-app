# Задача 6.2.2 — Единый формат ошибок Problem Details (RFC 9457)

## Описание
Сделать единый формат ответов об ошибках валидации (422) по стандарту Problem Details с медиатипом `application/problem+json` и задокументировать его в OpenAPI.

## Задачи
1. **Модель `ProblemDetails`** (Pydantic) с полями `type`, `title`, `status`, `detail`, `instance` и опциональным `errors: list[...]` для деталей по полям.
2. **Кастомный обработчик `RequestValidationError`:**
   - тело ответа соответствует модели Problem Details;
   - заголовок `Content-Type: application/problem+json`;
   - поле `errors` формируется из `exc.errors()` (поле, сообщение, код ошибки).
3. **Документация 422 в OpenAPI:** в декораторе маршрута добавить `responses={422: ...}` с `content["application/problem+json"]`, привязать модель и добавить `examples`.
4. **Минимальный API:** `POST /users` с `response_model` для успеха и задокументированным ответом 422.
5. **Проверка в Swagger UI:** видны схема Problem Details и примеры для 200 и 422.

## Пример
**Валидный запрос:**
```json
{
  "username": "alice",
  "age": 25,
  "email": "alice@example.com",
  "password": "s3cur3p4ss",
  "phone": "+7 999 123-45-67"
}
```
→ 200 OK `{"id": 1, "username": "alice"}`.

**Невалидный запрос:**
```json
{
  "username": "alice",
  "age": 17,
  "email": "not-an-email",
  "password": "short",
  "phone": "Unknown"
}
```
→ 422 `application/problem+json`:
```json
{
  "type": "https://example.com/problems/validation-error",
  "title": "Validation Error",
  "status": 422,
  "detail": "The request body failed validation.",
  "instance": "/users",
  "errors": [
    {"field": "age", "message": "ensure this value is greater than 18", "code": "value_error.number.not_gt"},
    {"field": "email", "message": "value is not a valid email address", "code": "value_error.email"},
    {"field": "password", "message": "ensure this value has at least 8 characters", "code": "value_error.any_str.min_length"}
  ]
}
```

## Критерии приёмки
- Все ответы 422 возвращаются с `application/problem+json` и единой структурой.
- В Swagger видны схема Problem Details, пример 200 и пример 422.

> Материалы: [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html), [FastAPI: RequestValidationError](https://fastapi.tiangolo.com/tutorial/handling-errors/).
