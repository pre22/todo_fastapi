from fastapi import APIRouter, Depends, HTTPException
from schemas.users import UserCreate
from models.users import User
from database.connection import get_session
from sqlmodel import Session, select
from passlib.context import CryptContext
from auth.jwt import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate, session: Session = Depends(get_session)):
    hashed_pw = pwd_context.hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_pw)
    session.add(db_user)
    session.commit()
    return {"msg": "user Created"}

@router.post("/login")
def login(user: UserCreate, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token}