from fastapi import FastAPI
from app.routes import auth as auth_routes
from app.routes import todos as todo_routes
from app.admin import router as admin_router
from app.websocket import router as ws_router
from app.database import init_db
from middleware import log_middleware


app = FastAPI()
# Init DB
init_db()

# Register router
app.include_router(auth_routes.router, prefix="/auth")
app.include_router(todo_routes.router, prefix="/todos")
app.include_router(admin_router)
app.include_router(ws_router)

# Register Middleware
app.middleware("http")(log_middleware)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)