from uuid import UUID, uuid4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.connection import Base
from models.users import User

class Todo(Base):
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        insert_default=uuid4,
        index=True
    )
    title: Mapped[str]
    completed: Mapped[bool]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="todos")


