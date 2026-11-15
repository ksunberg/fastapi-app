# Задача 5.3.3 — Ветвление и слияние миграций Alembic

## Описание
В крупных проектах миграции Alembic могут развиваться параллельно в разных «ветках» схемы базы данных. Alembic поддерживает собственный механизм ветвления и слияния ревизий, однако при этом могут возникать конфликты в порядке применения скриптов.

В предыдущем задании вы создали в проекте FastAPI модель `Product` и с помощью Alembic применили миграцию, которая создала таблицу `product` с полями `id`, `title`, `price`, `count`, `description`, `status` (`Enum`).

Теперь предстоит отработать ветвление и слияние ревизий: создать две независимые миграции, которые по-разному меняют одну и ту же таблицу, столкнуться с ошибкой `Multiple heads` и разрешить её через `alembic merge`.

## Шаг 1. Параллельные ревизии

### Ревизия A — добавление логического флага
В `models.py` для `Product` добавьте поле:

```python
# импорты те же
from sqlalchemy import Boolean, false

# …
is_featured: Mapped[bool] = mapped_column(
    Boolean, nullable=False, server_default=false()
)
```

Сгенерируйте новую ревизию с собственным идентификатором:

```bash
alembic revision --autogenerate -m "Add is_featured flag" --rev-id a2_featured
```

Убедитесь, что в `alembic/versions/a2_featured.py` есть:

```python
revision = 'a2_featured'
down_revision = '…_add_status_enum_to_product'  # идентификатор предыдущей миграции

# …
op.add_column(
    'product',
    sa.Column('is_featured', sa.Boolean(), nullable=False, server_default=sa.false()),
)
```

> Запомните идентификатор предыдущей миграции — он понадобится в ветке B.

Оставьте миграцию неприменённой (не запускайте `alembic upgrade`).

### Ревизия B — изменение существующего поля
В `models.py` измените поле `description` на тип `Text` и сделайте его обязательным:

```python
from sqlalchemy import Text

# …
description: Mapped[str] = mapped_column(Text, nullable=False)
```

Создайте пустую ревизию (без `--autogenerate`):

```bash
alembic revision -m "Alter description to Text" --rev-id b2_description
```

В `alembic/versions/b2_description.py` вручную пропишите шапку — `down_revision` должен совпадать с веткой A:

```python
revision = 'b2_description'
down_revision = '…_add_status_enum_to_product'  # тот же идентификатор, что и в ветке A
```

В функции `upgrade()` опишите изменение:

```python
def upgrade() -> None:
    op.alter_column(
        'product',
        'description',
        existing_type=sa.String(length=255),
        type_=sa.Text(),
        nullable=False,
    )
```

А в `downgrade()` — обратное:

```python
def downgrade() -> None:
    op.alter_column(
        'product',
        'description',
        existing_type=sa.Text(),
        type_=sa.String(length=255),
        nullable=True,
    )
```

Эту ревизию также оставьте неприменённой.

В каталоге `alembic/versions/` теперь должно быть две новых ревизии, у обеих в шапке `down_revision` равен идентификатору предыдущей миграции.

## Шаг 2. Обнаружение конфликта

Выполните:

```bash
alembic upgrade head
```

Вы получите сообщение об ошибке:

```text
Error: Multiple heads found: a2_featured, b2_description
Hint: run 'alembic merge'
```

Это означает, что Alembic нашёл две «головы» миграций и не знает, в каком порядке их применять.

## Шаг 3. Слияние веток миграций

Создайте merge-ревизию, объединив обе линии:

```bash
alembic merge -m "Merge branches" a2_featured b2_description --rev-id m2_merge
```

Откройте `alembic/versions/m2_merge.py` и убедитесь, что:

- в шапке файла указано:

  ```python
  revision = 'm2_merge'
  down_revision = ('a2_featured', 'b2_description')
  ```

- в функциях `upgrade()` и `downgrade()` ничего нет (`pass`) — `m2_merge` лишь соединяет ветки и не дублирует операции.

## Шаг 4. Проверка итоговой истории

Сбросьте базу до изначального состояния:

```bash
alembic downgrade base
```

Накатите всю цепочку миграций:

```bash
alembic upgrade head
```

Убедитесь, что таблица `product` теперь имеет и столбец `is_featured`, и обновлённый `description`.

Откатите все миграции:

```bash
alembic downgrade base
```

Все добавленные и изменённые элементы должны быть удалены без ошибок.

## Итоговые требования

В папке `alembic/versions/` должны присутствовать файлы:

- `0001_initial.py` — из первого задания;
- ревизии из прошлого этапа (`…_add_status_enum_to_product.py`);
- `a2_featured.py`, `b2_description.py`, `m2_merge.py`.

Файл `m2_merge.py` должен корректно объединять две ветви (правильные `down_revision`).

Должны успешно отрабатывать команды:

- `alembic upgrade head` после merge;
- `alembic downgrade base` для полного отката.

> Материалы: [Alembic Branches](https://alembic.sqlalchemy.org/en/latest/branches.html), [alembic merge](https://alembic.sqlalchemy.org/en/latest/commands.html#merge).
