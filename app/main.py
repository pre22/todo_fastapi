from fastapi import FastAPI
from app.routes import auth as auth_routes

app = FastAPI()

app.include_router(auth_routes.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)