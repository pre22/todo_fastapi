from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase
from decouple import config

DATABASE_URL  = "sqlite:///./todo.db"

engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    echo=config("echo", default=False)
),

connection = engine.connect()


class Base(DeclarativeBase):
    pass

# pool_size: How many active DB connections should SQLAlchemy keep available at all times?
# max_overflow: Number of extra temporary connections allowed beyond pool_size
# echo=True: SQLAlchemy will print all SQL statements it sends to the database.