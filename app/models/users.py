from uuid import UUID, uuid4
from typing import List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.connection import Base


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[UUID] = mapped_column(primary_key=True, insert_default=uuid4, init=False)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[Optional[str] | None]
    hashed_password: Mapped[str]

    addresses: Mapped[List["Address"]] = relationship(back_populates="user")
    todos: Mapped[List["Todo"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"


class Address(Base):
    __tablename__ = "address"

    id: Mapped[UUID] = mapped_column(primary_key=True, insert_default=uuid4, init=False)
    address: Mapped[str]
    user_id: Mapped[User] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, address={self.address!r})"


