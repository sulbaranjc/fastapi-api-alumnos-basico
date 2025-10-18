# alumnos_api/core/security.py

from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import Optional

JWT_SECRET = "supersecreto123"  # ⚠️ Reemplaza esto por una variable de entorno en producción
JWT_ALGORITHM = "HS256"

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> str:
        credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(request)
        if not credentials or credentials.scheme != "Bearer":
            raise HTTPException(status_code=403, detail="Token inválido")
        return self.verify_token(credentials.credentials)

    def verify_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            username = payload.get("sub")
            if not isinstance(username, str):
                raise HTTPException(status_code=403, detail="Token sin usuario válido")
            return username
        except JWTError:
            raise HTTPException(status_code=403, detail="Token inválido o expirado")
