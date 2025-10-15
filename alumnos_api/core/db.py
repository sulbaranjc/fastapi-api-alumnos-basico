from sqlmodel import SQLModel, create_engine, Session
from fastapi import HTTPException
from .config import settings

# Crear el engine de SQLAlchemy
DATABASE_URL = (
    f"mysql+pymysql://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600,
    echo=False  # Cambia a True para debug SQL
)

def create_db_and_tables():
    """Crear todas las tablas definidas en SQLModel"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency para obtener una sesión de base de datos"""
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {e}")
        finally:
            session.close()

# Función legacy para compatibilidad (se puede remover después)
def get_connection():
    """Función de compatibilidad - usar get_session() en su lugar"""
    import pymysql
    from pymysql.cursors import DictCursor
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
