# ----------------------------------------------------------
# main.py - API CRUD + CORS para frontend (React, etc.)
# ----------------------------------------------------------

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
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

# ------------------ Modelos (entrada/salida) --------------
def _nota_field():
    return Field(..., ge=0.0, le=10.0, description="Rango permitido: 0.0 a 10.0")

class AlumnoIn(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    nota1: float = _nota_field()
    nota2: float = _nota_field()
    nota3: float = _nota_field()
    notaFinal: float = _nota_field()

    @validator("nombre")
    def limpiar_nombre(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("El nombre no puede estar vacío.")
        return v

class AlumnoOut(BaseModel):
    id: int
    nombre: str
    nota1: float
    nota2: float
    nota3: float
    notaFinal: float
    promedioFinal: float

# ------------------ Utilidad de negocio -------------------
def calcular_promedio(n1: float, n2: float, n3: float, examen: float) -> float:
    continua = (n1 + n2 + n3) / 3.0
    return round(continua * 0.7 + examen * 0.3, 2)

# ------------------ App FastAPI ---------------------------
app = FastAPI(
    title="API CRUD Alumnos",
    version="1.1.0",
    description="Base + health + CRUD alumnos + CORS para frontend.",
)

# ------------------ CORS ----------------------------------
# Lista blanca de orígenes permitidos (ajústala a tus necesidades)
# Agrega aquí tu(s) dominio(s) de producción cuando los tengas.
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # usa ["*"] solo si NO usas credenciales
    allow_credentials=True,         # cookies/autenticación del navegador
    allow_methods=["*"],            # GET, POST, PUT, DELETE, OPTIONS, etc.
    allow_headers=["*"],            # Authorization, Content-Type, etc.
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

# ------------------ LISTAR ALUMNOS ------------------------
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
            rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar alumnos: {e}")

# ------------------ OBTENER POR ID ------------------------
@app.get("/alumnos/{alumno_id}", response_model=AlumnoOut)
def obtener_alumno(alumno_id: int):
    """Devuelve un alumno por su ID."""
    sql = "SELECT id, nombre, nota1, nota2, nota3, notaFinal, promedioFinal FROM alumnos WHERE id = %s"
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(sql, (alumno_id,))
            row = cur.fetchone()
        conn.close()
        if not row:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        return row
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener alumno: {e}")

# ------------------ CREAR -------------------------------
@app.post("/alumnos", response_model=AlumnoOut, status_code=201)
def crear_alumno(data: AlumnoIn):
    """
    Crea un alumno nuevo. `promedioFinal` se calcula automáticamente.
    """
    promedio = calcular_promedio(data.nota1, data.nota2, data.nota3, data.notaFinal)
    sql = """
        INSERT INTO alumnos (nombre, nota1, nota2, nota3, notaFinal, promedioFinal)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(sql, (data.nombre, data.nota1, data.nota2, data.nota3, data.notaFinal, promedio))
            nuevo_id = cur.lastrowid
        conn.commit()
        conn.close()
        return AlumnoOut(
            id=nuevo_id,
            nombre=data.nombre,
            nota1=data.nota1,
            nota2=data.nota2,
            nota3=data.nota3,
            notaFinal=data.notaFinal,
            promedioFinal=promedio
        )
    except Exception as e:
        try:
            conn.rollback()
            conn.close()
        except:
            pass
        raise HTTPException(status_code=500, detail=f"Error al crear alumno: {e}")

# ------------------ ACTUALIZAR ---------------------------
@app.put("/alumnos/{alumno_id}", response_model=AlumnoOut)
def actualizar_alumno(alumno_id: int, data: AlumnoIn):
    """
    Actualiza un alumno existente. Recalcula `promedioFinal`.
    """
    sql_get = "SELECT id FROM alumnos WHERE id = %s"
    sql_upd = """
        UPDATE alumnos
        SET nombre=%s, nota1=%s, nota2=%s, nota3=%s, notaFinal=%s, promedioFinal=%s
        WHERE id=%s
    """
    promedio = calcular_promedio(data.nota1, data.nota2, data.nota3, data.notaFinal)
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(sql_get, (alumno_id,))
            if not cur.fetchone():
                conn.close()
                raise HTTPException(status_code=404, detail="Alumno no encontrado")
            cur.execute(sql_upd, (data.nombre, data.nota1, data.nota2, data.nota3, data.notaFinal, promedio, alumno_id))
        conn.commit()
        conn.close()
        return AlumnoOut(
            id=alumno_id,
            nombre=data.nombre,
            nota1=data.nota1,
            nota2=data.nota2,
            nota3=data.nota3,
            notaFinal=data.notaFinal,
            promedioFinal=promedio
        )
    except HTTPException:
        raise
    except Exception as e:
        try:
            conn.rollback()
            conn.close()
        except:
            pass
        raise HTTPException(status_code=500, detail=f"Error al actualizar alumno: {e}")

# ------------------ ELIMINAR -----------------------------
@app.delete("/alumnos/{alumno_id}")
def eliminar_alumno(alumno_id: int):
    """Elimina un alumno por ID. Devuelve indicador de borrado."""
    sql = "DELETE FROM alumnos WHERE id=%s"
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(sql, (alumno_id,))
            afectados = cur.rowcount
        conn.commit()
        conn.close()
        if afectados == 0:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        return {"deleted": True, "id": alumno_id}
    except HTTPException:
        raise
    except Exception as e:
        try:
            conn.rollback()
            conn.close()
        except:
            pass
        raise HTTPException(status_code=500, detail=f"Error al eliminar alumno: {e}")

# ------------------ Arranque local opcional ---------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
