# The schema is used to filter and validate data from and to your tables respectively
from uuid import UUID
from pydantic import BaseModel
from typing import Optional


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class Todo(TodoBase):
    id: UUID
    completed: bool
    user_id: UUID

    class Config:
        from_attributes = True
