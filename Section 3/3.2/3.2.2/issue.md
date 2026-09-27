# Задача 3.2.2 — Подписанные cookie (itsdangerous)

## Описание
Расширить cookie-аутентификацию: подписывать значение `session_token`, чтобы клиент не мог его подделать.

## Формат cookie
```
<user_id>.<signature>
```

- `<user_id>` — уникальный идентификатор (например, UUID по стандарту RFC 4122; либо строка не короче 8 символов из латинских букв и цифр).
- `<signature>` — криптографическая подпись `user_id` секретным ключом (библиотека `itsdangerous`).

## Задачи
1. Создать маршрут `POST /login`: при успешной проверке сформировать строку `session_token` и установить cookie с параметрами `httponly=True` и подходящим `max_age`.
2. Создать защищённый маршрут (например, `GET /profile`):
   - считать cookie `session_token`;
   - проверить подпись тем же секретным ключом;
   - при успехе вернуть профиль, иначе — 401 с `{"message": "Unauthorized"}`.
3. Проверить работу с корректными и некорректными значениями cookie.

## Материалы для изучения
- [itsdangerous (PyPI)](https://pypi.org/project/itsdangerous/)
- [UUID — разница с GUID](https://ru.stackoverflow.com/questions/994093/)
- [Что делает itsdangerous](https://stackoverflow.com/questions/30938535/what-does-itsdangerous-do-to-sign-the-string)
