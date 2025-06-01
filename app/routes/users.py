from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from schemas.todo import TodoCreate, Todo, TodoUpdate
from schemas.users import UserCreate
from crud.todo import create_todo, get_todo, get_todos, update_todo as ut, delete_todo as dt
from crud.users import get_user_by_email, create_user

from auth.dependencies import get_current_active_user
from auth.utils import verify_password, create_access_token
from config import settings
from database.connection import get_sync_db

from models import todos as tmodels
from models.users import User

router = APIRouter()


@router.post("/", response_model=User)
def create_user(user: UserCreate, db=Depends(get_sync_db)):
    db_user = get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return create_user(db=db, user=user)

@router.get("/me", response_model=User)
def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.post("/token")
def login_for_access_token(
    db=Depends(get_sync_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = get_user_by_email(db, email=form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}