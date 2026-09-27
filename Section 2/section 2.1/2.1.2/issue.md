# Задача 2.1.2 — HTML-страница в FastAPI

## Описание
Создать FastAPI-приложение, которое отдаёт HTML-страницу по корневому адресу.

## Задачи
1. Создать html-файл (например, `index.html`):

```html
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Пример простой страницы html</title>
</head>
<body>
Я НЕРЕАЛЬНО КРУТ И МОЙ РЕСПЕКТ БЕЗ МЕРЫ :)
</body>
</html>
```

2. Создать приложение FastAPI с GET-обработчиком `/`, возвращающим HTML-страницу.
3. Запустить приложение:

```bash
uvicorn main:app --reload
```

4. Открыть `http://localhost:8000` в браузере.

> Подсказка: для возврата файла используйте возможности `FileResponse`.
