# Задача 3.1.2 — Продукты: путь и поиск

## Описание
Создать приложение FastAPI с двумя эндпоинтами для работы с продуктами.

## Эндпоинты
1. **Получение продукта** — `GET /product/{product_id}`
   - `product_id` — идентификатор продукта (целое число).
   - Ответ: JSON с информацией о продукте.

2. **Поиск товаров** — `GET /products/search`
   - `keyword` (str, обязательный) — ключевое слово для поиска.
   - `category` (str, необязательный) — категория для фильтрации.
   - `limit` (int, необязательный) — максимум товаров в ответе (по умолчанию 10).
   - Ответ: массив JSON с подходящими продуктами.

## Пример данных
```python
sample_products = [
    {"product_id": 123, "name": "Smartphone",  "category": "Electronics", "price": 599.99},
    {"product_id": 456, "name": "Phone Case",  "category": "Accessories", "price": 19.99},
    {"product_id": 789, "name": "Iphone",      "category": "Electronics", "price": 1299.99},
    {"product_id": 101, "name": "Headphones",  "category": "Accessories", "price": 99.99},
    {"product_id": 202, "name": "Smartwatch",  "category": "Electronics", "price": 299.99},
]
```

## Примеры
- `GET /product/123` → продукт Smartphone.
- `GET /products/search?keyword=phone&category=Electronics&limit=5` → Smartphone и Iphone.

> ⚠️ Важно: маршруты обрабатываются в порядке объявления. Если сначала объявить `/products/{product_id}`, то `/products/search` работать не будет — слово `search` не преобразуется в `int`. Обработчики обрабатываются в порядке объявления.
