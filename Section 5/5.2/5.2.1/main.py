from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
from models import TodoUpdate, TodoCreate, TodoResponse, TodoTable

app = FastAPI()

DATABASE_URL = "postgresql+psycopg://superuser:superpassword@127.0.0.1/postgres"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

#TODO сделать тест модульный
async def get_db():
    async with async_session_maker() as session:
        yield session

@app.post("/todos/", response_model=TodoResponse)
async def create_todo(todo: TodoCreate, db: AsyncSession = Depends(get_db)):
    db_todo = TodoTable(
        title=todo.title,
        description=todo.description,
        completed=False
    )
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

@app.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TodoTable).where(TodoTable.id == todo_id))
    todo = result.scalar_one_or_none()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo не найден")
    return todo

@app.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(
        todo_id: int,
        todo_update: TodoUpdate,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(TodoTable).where(TodoTable.id == todo_id))
    db_todo = result.scalar_one_or_none()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo не найден")
    if todo_update.title is not None:
        db_todo.title = todo_update.title
    if todo_update.description is not None:
        db_todo.description = todo_update.description
    if todo_update.completed is not None:
        db_todo.completed = todo_update.completed
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TodoTable).where(TodoTable.id == todo_id))
    db_todo = result.scalar_one_or_none()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo не найден")
    await db.delete(db_todo)
    await db.commit()
    return {"message": f"Todo успешно удален"}
