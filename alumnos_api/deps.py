"""
Dependencias para FastAPI con SQLModel
"""
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from .core.db import get_session

# Tipo anotado para la sesión de base de datos
SessionDep = Annotated[Session, Depends(get_session)]

# Función helper para usar en routers
def get_db_session() -> Session:
    """
    Dependency function para obtener una sesión de base de datos.
    Usar SessionDep en su lugar para type hints más limpios.
    """
    return Depends(get_session)
