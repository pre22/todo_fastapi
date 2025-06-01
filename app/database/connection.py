from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


from config import settings

# For SQLite (or other databases)
SQLALCHEMY_DATABASE_URL = settings.database_url

# For async databases (PostgreSQL, MySQL)
ASYNC_SQLALCHEMY_DATABASE_URL = settings.async_database_url

# Synchronous engine (for SQLite, development)
sync_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite specific
    echo=True  # Log SQL queries (disable in production)
)

# Async engine (for production databases)
async_engine = create_async_engine(
    ASYNC_SQLALCHEMY_DATABASE_URL,
    echo=True
)


# Session factories
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=sync_engine)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Sync Dependency
def get_sync_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Async dependency
async def get_async_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()








class Base(DeclarativeBase):
    pass

# pool_size: How many active DB connections should SQLAlchemy keep available at all times?
# max_overflow: Number of extra temporary connections allowed beyond pool_size
# echo=True: SQLAlchemy will print all SQL statements it sends to the database.