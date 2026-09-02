from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    class Config:
        env_file = Path(__file__).parent / ".env"


settings = Settings()
