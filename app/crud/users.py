from uuid import UUID
from sqlalchemy.orm import Session

from models.users import User
from schemas import users as users_schemas

from auth.utils import get_password_hash

def get_user(db: Session, user_id: UUID):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: users_schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: UUID, user: users_schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if db_user is None:
        return None
    
    user_data = user.dict(exclude_unset=True)
    
    if "password" in user_data:
        hashed_password = get_password_hash(user_data["password"])
        del user_data["password"]
        user_data["hashed_password"] = hashed_password

    for field, value in user_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: UUID):
    db_user = get_user(db, user_id)

    if db_user is None:
        return None
    
    db.delete(db_user)
    db.commit()
    return db_user
