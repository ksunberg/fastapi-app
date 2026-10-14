# Задача 5.2.2 — Todo: пагинация, фильтрация, аналитика

## Описание
Расширить Todo-лист продвинутыми функциями: пагинация, фильтрация, сортировка, аналитика и массовое обновление. Рекомендуется БД PostgreSQL.

## Требования

### 1. Пагинация и сортировка — `GET /todos`
Параметры:
- `limit` — макс. элементов на странице (по умолчанию 10, максимум 100);
- `offset` — смещение (по умолчанию 0);
- `sort_by` — поле сортировки: `-created_at` (desc), `title` (asc).

```http
GET /todos?limit=5&offset=10&sort_by=-created_at
```

### 2. Расширенная фильтрация
- `completed` — true/false;
- `created_after`, `created_before` — даты в формате `YYYY-MM-DD` (время 00:00:00);
- `title_contains` — поиск подстроки без учёта регистра.

```http
GET /todos?completed=false&created_after=2024-03-01&title_contains=urgent
```

### 3. Аналитика — `GET /todos/analytics`
Параметр `timezone` (например, `Europe/Moscow`). Невалидная таймзона → ошибка 400.

Рассчитать:
- общее количество задач;
- `completed_stats: {"true": 30, "false": 70}`;
- среднее время выполнения завершённых задач в часах;
- распределение по дням недели: `weekday_distribution: {"Monday": 15, ...}`.

```http
GET /todos/analytics?timezone=Europe/Moscow
```

### 4. Массовое обновление — `PATCH /todos`
```http
PATCH /todos?ids=1,2,3&completed=true
```
Ответ: `{"updated_count": 3}`. Несуществующие `id` пропускаются.

## Технические требования
1. **Модель Todo** дополнить полями `created_at` (TIMESTAMP, авто) и `completed_at` (TIMESTAMP, при `completed = true`).
2. **SQL:** `WHERE`, `BETWEEN`, `ILIKE`, `ORDER BY`, `COUNT()`, `AVG()`, `EXTRACT(DOW FROM created_at)`.
3. **Валидация:** формат дат `YYYY-MM-DD`, `limit ≤ 100`.
4. **Безопасность:** параметризованные запросы против SQL-инъекций.

## Пример ответа аналитики
```json
{
  "total": 150,
  "completed_stats": {"true": 60, "false": 90},
  "avg_completion_time_hours": 24.5,
  "weekday_distribution": {"Monday": 25, "Tuesday": 30, "Wednesday": 20, "Thursday": 35, "Friday": 40, "Saturday": 0, "Sunday": 0}
}
```

## Критерии успеха
- Все параметры (`limit`, `offset`, фильтры) работают совместно.
- Аналитические запросы ≤ 100 мс на 10k записей.
- Swagger описывает новые параметры.
- Проверяются: несуществующие ID, некорректный `limit` (150), пустые результаты, конвертация таймзон.
