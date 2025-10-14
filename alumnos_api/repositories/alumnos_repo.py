from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from ..services.alumnos_service import calcular_promedio

def listar(conn) -> List[Dict[str, Any]]:
    with conn.cursor() as cur:
        cur.execute("""SELECT id, nombre, nota1, nota2, nota3, notaFinal, promedioFinal
                       FROM alumnos ORDER BY id DESC""")
        return cur.fetchall()

def obtener(conn, alumno_id: int) -> Dict[str, Any]:
    with conn.cursor() as cur:
        cur.execute("""SELECT id, nombre, nota1, nota2, nota3, notaFinal, promedioFinal
                       FROM alumnos WHERE id=%s""", (alumno_id,))
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return row

def crear(conn, data) -> Dict[str, Any]:
    promedio = calcular_promedio(data.nota1, data.nota2, data.nota3, data.notaFinal)
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO alumnos (nombre, nota1, nota2, nota3, notaFinal, promedioFinal)
                       VALUES (%s,%s,%s,%s,%s,%s)""",
                    (data.nombre, data.nota1, data.nota2, data.nota3, data.notaFinal, promedio))
        nuevo_id = cur.lastrowid
    conn.commit()
    return {**data.dict(), "id": nuevo_id, "promedioFinal": promedio}

def actualizar(conn, alumno_id: int, data) -> Dict[str, Any]:
    # asegurar existencia
    obtener(conn, alumno_id)
    promedio = calcular_promedio(data.nota1, data.nota2, data.nota3, data.notaFinal)
    with conn.cursor() as cur:
        cur.execute("""UPDATE alumnos
                       SET nombre=%s, nota1=%s, nota2=%s, nota3=%s, notaFinal=%s, promedioFinal=%s
                       WHERE id=%s""",
                    (data.nombre, data.nota1, data.nota2, data.nota3, data.notaFinal, promedio, alumno_id))
    conn.commit()
    return {"id": alumno_id, **data.dict(), "promedioFinal": promedio}

def eliminar(conn, alumno_id: int) -> bool:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM alumnos WHERE id=%s", (alumno_id,))
        afectados = cur.rowcount
    conn.commit()
    if afectados == 0:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return True
