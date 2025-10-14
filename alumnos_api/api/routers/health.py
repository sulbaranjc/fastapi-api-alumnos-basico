from fastapi import APIRouter
from ...core.db import get_connection

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
def root():
    return {"api": "OK"}

@router.get("/db")
def db():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 AS ok")
            row = cur.fetchone()
        return {"db": "up" if row and row.get("ok") == 1 else "unknown"}
    finally:
        conn.close()
