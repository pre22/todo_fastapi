from pydantic import BaseModel


class TodoCreate(BaseModel):
    title: str


class TodoOut(BaseModel):
    id: int
    title: str
    completed: bool
