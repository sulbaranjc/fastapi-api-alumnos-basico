# alumnos_api/api/routers/auth.py

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta

from alumnos_api.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

# Usuario hardcodeado (por ahora, en memoria)
USER_DB = {
    "admin": {
        "username": "admin",
        "password": "admin123",  # para pruebas (en producción usar hash)
    }
}

# Secretos y expiración
JWT_SECRET = "supersecreto123"  # En producción ponerlo en .env
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    user = USER_DB.get(data.username)
    if not user or data.password != user["password"]:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {
        "sub": data.username,
        "exp": expire
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return {"access_token": token}
