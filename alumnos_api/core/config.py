# alumnos_api/core/config.py
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    app_name: str = "API CRUD Alumnos"
    version: str = "2.0.0"

    db_host: str
    db_port: int = 3306
    db_user: str
    db_password: str
    db_name: str

    # Valor por defecto (sirve si no defines ALLOWED_ORIGINS en .env)
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5500",
    ]

    # ✅ Acepta JSON o CSV en .env (pydantic v2)
    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v):
        if isinstance(v, str):
            s = v.strip()
            if not s:
                return []
            if s.startswith("["):   # JSON válido
                return s
            # CSV simple: "http://a:3000,http://b:5173"
            return [x.strip() for x in s.split(",") if x.strip()]
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()  # type: ignore[call-arg]
