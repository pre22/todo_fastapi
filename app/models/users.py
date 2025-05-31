from uuid import UUID, uuid4
from typing import List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.connection import Base


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[UUID] = mapped_column(primary_key=True, insert_default=uuid4, init=False)
    name: Mapped[str] = mapped_column(String(30))
    username: Mapped[Optional[str] | None]

    addresses = Mapped[List["Address"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"

    id: Mapped[UUID] = mapped_column(primary_key=True, insert_default=uuid4, init=False)
    email_address: Mapped[str]
    user_id: Mapped[User] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


