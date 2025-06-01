from uuid import UUID
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload, Session

from models.todos import Todo
from models.users import User

from schemas import todo as todo_schemas


async def get_todo(db: Session, todo_id: UUID):
    return db.query(Todo).filter(Todo.id == todo_id).first()

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Todo).offset(skip).limit(limit).all()

def create_todo(db: Session, todo: todo_schemas.TodoCreate, user_id: UUID):
    db_todo = Todo(**todo.dict(), user_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo_id: UUID, todo: todo_schemas.TodoUpdate):
    db_todo = get_todo(db, todo_id)
    if db_todo is None:
        return None
    for field, value in todo.dict(exclude_unset=True).items():
        setattr(db_todo, field, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: UUID):
    db_todo = get_todo(db, todo_id)
    if db_todo is None:
        return None
    db.delete(db_todo)
    db.commit()
    return db_todo