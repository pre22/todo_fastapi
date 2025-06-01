import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from alembic import command
from alembic.config import Config
from config import settings
from contextlib import asynccontextmanager
from decouple import Config as cfg

from routes import todos as todo_routes
from admin import router as admin_router
from websocket import router as ws_router

from database.connection import async_engine, sync_engine, get_async_db



async def run_migrations():
    """Run Alembic migrations programmatically."""

    try:
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", cfg("database_url"))
        command.upgrade(alembic_cfg, "head")
        return True
    except Exception as e:
        print(f"Migrations failed: {e}")
        return False


@asynccontextmanager
async def lifespan(app: FastAPI):

    if cfg("debug") == "True": # Development
        sync_engine.dispose()
    
    else:
        await async_engine.dispose()
        
    yield

    await async_engine.dispose()


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan
)


@app.get("/healthcheck")
async def healthcheck(db: AsyncSession = Depends(get_async_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 500


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)





# Register router
app.include_router(todo_routes.router, prefix="/todos")
app.include_router(admin_router, prefix="/admin")
app.include_router(ws_router)




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)