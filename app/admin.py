from fastapi import APIRouter, Depends
from database.connection import get_session
from models.users import User
from models.todos import Todo
from sqlmodel import Session, select

router = APIRouter()

@router.get("/stats")
def get_stats(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    todos = session.exec(select(Todo)).all()
    return {"users": len(users), "todos": len(todos)}