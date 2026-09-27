# Задача 4.1.2 — Хеширование паролей и защита от тайминг-атак

## Описание
Переиспользовать код из предыдущего задания (принцип DRY) и добавить безопасную аутентификацию: хеширование паролей через PassLib/Bcrypt и защиту от тайминг-атак.

## Модели данных
- `UserBase` — поле `username` (str, обязательное).
- `User(UserBase)` — дополнительно поле `password` (str).
- `UserInDB(UserBase)` — дополнительно поле `hashed_password` (str). Открытый пароль в этой модели хранить нельзя — только хеш.

## Задачи
1. **PassLib:** инициализировать `CryptContext` с алгоритмом Bcrypt для генерации и проверки хешей.
2. **Зависимость `auth_user`:**
   - извлекает `username`/`password` из заголовка `Authorization` через `HTTPBasicCredentials`;
   - ищет пользователя в in-memory базе `fake_users_db`;
   - проверяет пароль методом `verify` у `CryptContext`;
   - для сравнения логин-строк использует `secrets.compare_digest()`;
   - при успехе возвращает объект пользователя, иначе — `HTTPException` 401 с заголовком `WWW-Authenticate: Basic`.
3. **Маршруты:**
   - `POST /register` — принимает JSON по модели `User`, генерирует хеш, сохраняет `UserInDB` в `fake_users_db`, возвращает сообщение об успехе.
   - `GET /login` — через `Depends(auth_user)` возвращает `{"message": "Welcome, <username>!"}` при успехе; при ошибке — 401 с `WWW-Authenticate: Basic`.

## Тестирование через curl
```bash
# Регистрация
curl -X POST -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"correctpass"}' http://localhost:8000/register

# Успешный логин
curl -u user1:correctpass http://localhost:8000/login

# Неверный пароль
curl -u user1:wrongpass http://localhost:8000/login
```

> Материалы: [PassLib](https://passlib.readthedocs.io/), [FastAPI HTTP Basic Auth](https://fastapi.tiangolo.com/advanced/security/http-basic-auth/), [secrets.compare_digest](https://docs.python.org/3/library/secrets.html).
