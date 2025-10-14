# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    app_name: str = "API CRUD Alumnos"
    version: str = "2.0.0"

    db_host: str
    db_port: int = 3306
    db_user: str
    db_password: str
    db_name: str

    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # ignora vars extra del .env sin romper
    )

# app/core/config.py
settings = Settings()  # type: ignore[call-arg]

