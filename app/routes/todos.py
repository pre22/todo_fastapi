from fastapi import APIRouter, Depends
from schemas.todo import TodoCreate, TodoOut
from models.todos import Todo
from models.users import User
from database import get_session
from sqlmodel import Session
from auth.protected import get_current_user

router = APIRouter()

@router.post("/create", response_model=TodoOut)
def create_todo(todo: TodoCreate, username: str = Depends(get_current_user), session: Session = Depends(get_session)):
    db_todo = Todo(title=todo.title, owner_id=1)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo