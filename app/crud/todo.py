from uuid import UUID
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, Session

from models.todos import Todo
from models.users import User

from schemas import todo as todo_schemas


async def get_todo(db, todo_id: UUID):
    result = await db.execute(
        select(Todo)
        .where(Todo.id == todo_id)
    )
    return result.scalar_one_or_none()

async def get_todos(db, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Todo)
        .offset(skip)
    )
    return result.scalars().all()

async def create_todo(db, todo: todo_schemas.TodoCreate, user_id: UUID):
    db_todo = Todo(**todo.model_dump(), user_id=user_id)
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

async def update_todo(db, todo_id: UUID, todo: todo_schemas.TodoUpdate):
    result = await db.execute(
        update(Todo)
        .where(Todo.id == todo_id)
        .values(**todo.model_dump(exclude_unset=True))
        .returning(Todo)
    )
    await db.commit()
    return result.scalar_one()

async def delete_todo(db, todo_id: UUID):
    result = await db.execute(
        delete(Todo)
        .where(Todo.id == todo_id)
        .returning(Todo)
    )
    await db.commit()
    return result.scalar_one()