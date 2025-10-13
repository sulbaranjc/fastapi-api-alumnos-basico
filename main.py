# ----------------------------------------------------------
# main.py - API base + listar alumnos
# ----------------------------------------------------------

from fastapi import FastAPI, HTTPException
import pymysql
from pymysql.cursors import DictCursor

# ------------------ Config BD -----------------------------
DB_HOST = "192.168.1.251"
DB_PORT = 3306
DB_USER = "testuser"
DB_PASSWORD = "Jc10439536+"
DB_NAME = "crud_alumnos"

def get_connection():
    """Crea y devuelve una conexión a MySQL con timeouts cortos."""
    try:
        return pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=DictCursor,  # filas como dict
            charset="utf8mb4",
            connect_timeout=5,
            read_timeout=5,
            write_timeout=5,
            autocommit=False,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")

# ------------------ App FastAPI ---------------------------
app = FastAPI(
    title="API CRUD Alumnos - Paso 1",
    version="0.2.0",
    description="Base + health + listar alumnos.",
)

# ------------------ Endpoints base ------------------------
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
        return {"db": "unknown"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB down: {e}")

# ------------------ Nuevo: LISTAR ALUMNOS -----------------
@app.get("/alumnos")
def listar_alumnos():
    """
    Devuelve la lista completa de alumnos.
    Respuesta: array de objetos con los campos de la tabla.
    """
    sql = """
        SELECT id, nombre, nota1, nota2, nota3, notaFinal, promedioFinal
        FROM alumnos
        ORDER BY id DESC
    """
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()  # lista de dicts
        conn.close()
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar alumnos: {e}")

# ------------------ Arranque local opcional ---------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
