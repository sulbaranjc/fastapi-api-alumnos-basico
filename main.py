# ----------------------------------------------------------
# main.py - Versión base mínima
# API OK + Prueba de conexión MySQL (health check)
# ----------------------------------------------------------

from fastapi import FastAPI, HTTPException
import pymysql
from pymysql.cursors import DictCursor

# ----------------------------------------------------------
# Configuración de conexión a MySQL
# ----------------------------------------------------------
DB_HOST = "192.168.1.251"
DB_PORT = 3306
DB_USER = "testuser"
DB_PASSWORD = "Jc10439536+"
DB_NAME = "crud_alumnos"

def get_connection():
    """Crea y devuelve una conexión a la base de datos MySQL."""
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=DictCursor,
            charset="utf8mb4",
            connect_timeout=5,
            read_timeout=5,
            write_timeout=5,
        )
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")

# ----------------------------------------------------------
# Inicialización del API
# ----------------------------------------------------------
app = FastAPI(
    title="API CRUD Alumnos - Etapa 1",
    version="0.1.0",
    description="API mínima para probar conexión a MySQL y salud general.",
)

# ----------------------------------------------------------
# Endpoints básicos
# ----------------------------------------------------------

@app.get("/")
def root():
    """Verifica que la API esté operativa."""
    return {"api": "OK"}

@app.get("/health/db")
def health_db():
    """Verifica el estado de la conexión a MySQL."""
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT 1 AS ok")
            row = cur.fetchone()
        conn.close()

        if row and row.get("ok") == 1:
            return {"db": "up"}
        else:
            return {"db": "unknown"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB down: {e}")

# ----------------------------------------------------------
# Ejecución directa (opcional)
# ----------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
