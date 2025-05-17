import uuid
from sqlmodel import SQLModel, Field


class Todo(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    title: str
    completed: bool = False
    owner_id: int