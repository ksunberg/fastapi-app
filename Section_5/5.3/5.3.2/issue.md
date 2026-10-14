# Задача 5.3.2 — Enum-поля и ручная правка миграций

## Описание
Добавить в модель `Product` поле-перечисление (`Enum`) и научиться вручную корректировать миграции там, где автогенерация не справляется.

## Шаг 1. Добавление поля-Enum
В `models.py` добавить:

```python
from enum import Enum as PyEnum
from sqlalchemy import Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ProductStatus(PyEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Product(Base):
    # ... существующие поля ...
    status: Mapped[ProductStatus] = mapped_column(
        Enum(ProductStatus, name="product_status"),
        nullable=False,
        server_default=ProductStatus.DRAFT.value,
    )
```

Сгенерировать и применить миграцию:
```bash
alembic revision --autogenerate -m "Add status enum to product"
alembic upgrade head
```
Убедиться, что в схеме появились тип `product_status` и столбец `status`.

## Шаг 2. Расширение перечисления и ручная правка миграции
1. Добавить новое значение в `ProductStatus`: `DEPRECATED = "deprecated"`.
2. Сгенерировать миграцию:
```bash
alembic revision --autogenerate -m "Extend product_status enum"
```
3. Обратить внимание: Alembic **не** добавит код для обновления типа ENUM в PostgreSQL (автогенерация считает тип неизменным).
4. Открыть созданный файл миграции и **вручную** дописать в `upgrade()` и `downgrade()` SQL-команды (`ALTER TYPE ... ADD VALUE`). Обратите внимание, что `downgrade` будет достаточно сложным.
5. Применить миграцию и проверить, что записи могут получать `status='deprecated'`.

> Материалы: [SQLAlchemy Enum Columns](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum), [Alembic autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html), [ALTER TYPE … ADD VALUE](https://www.postgresql.org/docs/current/sql-altertype.html).
