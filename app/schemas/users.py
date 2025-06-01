from uuid import UUID
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[EmailStr] = None


class User(UserBase):
    id: UUID
    is_active: bool


    class Config:
        orm_mode = True
