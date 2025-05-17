from fastapi import FastAPI
from app.routes import auth as auth_routes
from middleware import log_middleware

app = FastAPI()

# Register router
app.include_router(auth_routes.router)
# Register Middleware
app.middleware("http")(log_middleware)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)