from fastapi import APIRouter, HTTPException
from ...core.db import get_connection
from ...schemas.alumno import AlumnoIn, AlumnoOut
from ...repositories import alumnos_repo as repo

router = APIRouter(prefix="/alumnos", tags=["alumnos"])

@router.get("")
def listar():
    conn = get_connection()
    try:
        return repo.listar(conn)
    finally:
        conn.close()

@router.get("/{alumno_id}", response_model=AlumnoOut)
def obtener(alumno_id: int):
    conn = get_connection()
    try:
        return repo.obtener(conn, alumno_id)
    finally:
        conn.close()

@router.post("", response_model=AlumnoOut, status_code=201)
def crear(data: AlumnoIn):
    conn = get_connection()
    try:
        row = repo.crear(conn, data)
        return AlumnoOut(**row)
    finally:
        conn.close()

@router.put("/{alumno_id}", response_model=AlumnoOut)
def actualizar(alumno_id: int, data: AlumnoIn):
    conn = get_connection()
    try:
        row = repo.actualizar(conn, alumno_id, data)
        return AlumnoOut(**row)
    finally:
        conn.close()

@router.delete("/{alumno_id}")
def eliminar(alumno_id: int):
    conn = get_connection()
    try:
        repo.eliminar(conn, alumno_id)
        return {"deleted": True, "id": alumno_id}
    finally:
        conn.close()
