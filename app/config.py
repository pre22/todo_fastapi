from pydantic_settings import BaseSettings
from decouple import config


class Settings(BaseSettings):
    app_name: str = "Todo API"
    admin_email: str
    database_url: str 
    async_database_url: str 
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    debug: bool

    class Config:
        env_file = ".env"
    

settings = Settings()