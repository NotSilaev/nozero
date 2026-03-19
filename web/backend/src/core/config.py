from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Project
    PROJECT_TITLE: str = "NOZERO"
    PROJECT_VERSION: str = "0.0.0"

    # Database
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # CORS
    CORS_ORIGINS: list

    # SMTP
    SMTP_HOST: str
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM: str

    # JWT
    JWT_ACCESS_SECRET: str
    JWT_REFRESH_SECRET: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TTL_SECONDS: int
    JWT_REFRESH_TTL_SECONDS: int

    # Cache
    CACHE_HOST: str
    CACHE_PORT: str
    CACHE_DB: str
    CACHE_MAX_CONNECTIONS: int

    class Config:
        env_file = Path(__file__).parent / ".env"


settings = Settings()
