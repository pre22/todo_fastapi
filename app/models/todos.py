from uuid import UUID, uuid4
from sqlalchemy import ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.connection import Base
from models.users import User

class Todo(Base):

    __tablename__ = "todos"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        insert_default=uuid4,
        index=True
    )
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="todos")


