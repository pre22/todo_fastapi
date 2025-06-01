from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import auth as auth_routes
from routes import todos as todo_routes
from admin import router as admin_router
from websocket import router as ws_router
from database.connection import async_engine, Base
from config import settings


app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


async def startup():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Register router
app.include_router(auth_routes.router, prefix="/auth")
app.include_router(todo_routes.router, prefix="/todos")
app.include_router(admin_router, prefix="/admin")
app.include_router(ws_router)




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)