from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from schemas.todo import TodoCreate, Todo, TodoUpdate
from schemas.users import UserCreate
from crud.todo import create_todo, get_todo, get_todos, update_todo as ut, delete_todo as dt

from auth.dependencies import get_current_active_user
from database.connection import get_db

from models import todos as tmodels
from models.users import User

router = APIRouter()

@router.post("/", response_model=Todo)
def create_todo(
    todo: TodoCreate,
    db=Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return create_todo(db=db, todo=todo, user_id=current_user.id)


@router.get("/", response_model=List[Todo])
def read_todos(
    skip: int = 0,
    limit: int = 100,
    db=Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    todos = get_todos(db, skip=skip, limit=limit)
    return todos


@router.get("/{todo_id}", response_model=Todo)
def read_todo(
    todo_id: UUID,
    db=Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    todo = get_todo(db, todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Access Denied")
    
    return todo

@router.put("/{todo_id}", response_model=Todo)
def update_todo(
    todo_id: UUID,
    todo: TodoUpdate,
    db=Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_todo = get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, details="Todo not found")
    
    if db_todo.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not Enough Permissions")
    
    return ut(db=db, todo_id=todo_id, todo=todo)

@router.delete("/{todo_id}", response_model=Todo)
def delete_todo(
    todo_id: UUID,
    db=Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_todo = get_todo(db, todo_id=todo_id)

    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not Found")
    
    if db_todo.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not Enough Permission")
    
    return dt(db=db, todo_id=todo_id)