from fastapi import APIRouter
from sqlmodel import text
from ...deps import SessionDep

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
def root():
    """Health check básico de la API"""
    return {"api": "OK"}

@router.get("/db")
def db(session: SessionDep):
    """Health check de la base de datos usando SQLModel"""
    try:
        result = session.exec(text("SELECT 1 AS ok")).first()
        return {"db": "up" if result and result[0] == 1 else "unknown"}
    except Exception as e:
        return {"db": "down", "error": str(e)}
