import pymysql
from pymysql.cursors import DictCursor
from fastapi import HTTPException
from .config import settings

def get_connection():
    try:
        return pymysql.connect(
            host=settings.db_host,
            port=settings.db_port,
            user=settings.db_user,
            password=settings.db_password,
            database=settings.db_name,
            cursorclass=DictCursor,
            charset="utf8mb4",
            connect_timeout=5, read_timeout=5, write_timeout=5,
            autocommit=False,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")
