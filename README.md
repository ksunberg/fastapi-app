# FastAPI Учебный Проект

Учебный бэкенд-сервис на FastAPI с JWT-авторизацией, ролевой моделью доступа и работой с PostgreSQL.

##  О проекте

Это учебный проект, который я создала, чтобы освоить FastAPI и связанные с ним технологии. Здесь реализованы базовые, но важные задачи, которые встречаются в большинстве бэкенд-приложений:

- **Аутентификация и авторизация** — регистрация, вход, JWT-токены, хеширование паролей, разделение прав (обычные пользователи и админы)
- **Работа с базами данных** — PostgreSQL, SQLAlchemy (ORM), миграции через Alembic
- **Валидация данных** — Pydantic-схемы для проверки входящих запросов
- **Документация API** — автоматическая Swagger-документация

Код написан аккуратно: файлы разложены по папкам, логика разделена на слои, есть комментарии к сложным участкам.


## Стек технологий

| Компонент | Технология |
|-----------|------------|
| Язык | Python 3.12 |
| Веб-фреймворк | FastAPI |
| Сервер | Uvicorn |
| ORM | SQLAlchemy 2.0 |
| Миграции | Alembic |
| База данных | PostgreSQL |
| Валидация | Pydantic v2 |
| Аутентификация | JWT + bcrypt |
| Тестирование | pytest |
| Контейнеризация | Docker + Docker Compose |


# Быстрый старт

### Клонировать репозиторий
    git clone https://github.com/ksunberg/fastapi-app.git
    cd fastapi-app

### Запустить контейнеры
    docker-compose up -d

После запуска:

    API: http://localhost:8000
    Swagger UI: http://localhost:8000/docs
    ReDoc: http://localhost:8000/redoc

### Остановить контейнеры:
    docker-compose down

Создайте файл .env в корне проекта со следующими настройками:
env

### Подключение к базе данных
    DATABASE_URL=postgresql://postgres:postgres@db:5432/fastapi_db

### Секретный ключ для JWT (сгенерируйте свой)
    SECRET_KEY=your-super-secret-key-change-this

### Режим отладки
    DEBUG=True

### Настройки базы данных (для локального запуска без Docker)
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=fastapi_db


### docker-compose.yml
      version: '3.8'
      
      services:
        db:
          image: postgres:15
          container_name: fastapi_db
          environment:
            POSTGRES_USER: postgres
            POSTGRES_PASSWORD: postgres
            POSTGRES_DB: fastapi_db
          ports:
            - "5432:5432"
          volumes:
            - postgres_data:/var/lib/postgresql/data
          healthcheck:
            test: ["CMD-SHELL", "pg_isready -U postgres"]
            interval: 5s
            timeout: 5s
            retries: 5

        app:
          build: .
          container_name: fastapi_app
          ports:
            - "8000:8000"
          depends_on:
            db:
              condition: service_healthy
          environment:
            DATABASE_URL: postgresql://postgres:postgres@db:5432/fastapi_db
            SECRET_KEY: ${SECRET_KEY:-your-secret-key-here}
            DEBUG: ${DEBUG:-True}
          volumes:
            - .:/app
          command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
      
      volumes:
        postgres_data:


Планы по развитию

    Написать тесты — покрыть основные эндпоинты (регистрация, вход, создание/получение данных) через pytest. Это покажет, что код не просто работает, а ещё и проверяется.

    Настроить логирование — добавить запись логов в файл, чтобы можно было отслеживать ошибки и действия пользователей. Например, кто и когда залогинился, какие запросы падали с ошибкой.

    Добавить пагинацию — при получении списка пользователей или других данных. Чтобы не выгружать все записи сразу, а выдавать по 10-20 штук с возможностью переключать страницы.

    Реализовать обработку ошибок — добавить человекочитаемые сообщения об ошибках вместо стандартных стектрейсов. Например, при неверном пароле выдавать "Неверный логин или пароль", а не внутреннюю ошибку сервера.
    
    Добавить валидацию на уровне БД — проверить, что все ограничения (уникальность email, длина полей) заданы и в моделях SQLAlchemy, чтобы данные не портились даже при случайных ошибках в коде.

### Контакты

Если у вас есть вопросы или предложения — свяжитесь со мной:
  
      GitHub: ksunberg
      Telegram: t.me/deathforedo66
      Email: koteeeeky@gmail.com
