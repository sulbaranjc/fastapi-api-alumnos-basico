from typing import List
from fastapi import APIRouter
from ...deps import SessionDep
from ...schemas.alumno import AlumnoIn, AlumnoOut
from ...repositories import alumnos_repo as repo

router = APIRouter(prefix="/alumnos", tags=["alumnos"])

@router.get("", response_model=List[AlumnoOut])
def listar(session: SessionDep):
    """Listar todos los alumnos"""
    return repo.listar(session)

@router.get("/{alumno_id}", response_model=AlumnoOut)
def obtener(alumno_id: int, session: SessionDep):
    """Obtener un alumno por ID"""
    return repo.obtener(session, alumno_id)

@router.post("", response_model=AlumnoOut, status_code=201)
def crear(data: AlumnoIn, session: SessionDep):
    """Crear un nuevo alumno"""
    return repo.crear(session, data)

@router.put("/{alumno_id}", response_model=AlumnoOut)
def actualizar(alumno_id: int, data: AlumnoIn, session: SessionDep):
    """Actualizar un alumno existente"""
    return repo.actualizar(session, alumno_id, data)

@router.delete("/{alumno_id}")
def eliminar(alumno_id: int, session: SessionDep):
    """Eliminar un alumno"""
    repo.eliminar(session, alumno_id)
    return {"deleted": True, "id": alumno_id}
