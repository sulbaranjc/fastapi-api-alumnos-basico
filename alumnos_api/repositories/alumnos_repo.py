from typing import List, Optional
from sqlmodel import Session, select, desc
from fastapi import HTTPException
from ..schemas.alumno import Alumno, AlumnoIn
from ..services.alumnos_service import calcular_promedio

def listar(session: Session) -> List[Alumno]:
    """Listar todos los alumnos ordenados por ID descendente"""
    statement = select(Alumno).order_by(desc(Alumno.id))
    return session.exec(statement).all()

def obtener(session: Session, alumno_id: int) -> Alumno:
    """Obtener un alumno por ID"""
    alumno = session.get(Alumno, alumno_id)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return alumno

def crear(session: Session, data: AlumnoIn) -> Alumno:
    """Crear un nuevo alumno"""
    promedio = calcular_promedio(data.nota1, data.nota2, data.nota3, data.notaFinal)
    
    # Crear instancia del modelo
    alumno = Alumno(
        nombre=data.nombre,
        nota1=data.nota1,
        nota2=data.nota2,
        nota3=data.nota3,
        notaFinal=data.notaFinal,
        promedioFinal=promedio
    )
    
    session.add(alumno)
    session.commit()
    session.refresh(alumno)
    return alumno

def actualizar(session: Session, alumno_id: int, data: AlumnoIn) -> Alumno:
    """Actualizar un alumno existente"""
    alumno = obtener(session, alumno_id)  # Verificar que existe
    
    promedio = calcular_promedio(data.nota1, data.nota2, data.nota3, data.notaFinal)
    
    # Actualizar campos
    alumno.nombre = data.nombre
    alumno.nota1 = data.nota1
    alumno.nota2 = data.nota2
    alumno.nota3 = data.nota3
    alumno.notaFinal = data.notaFinal
    alumno.promedioFinal = promedio
    
    session.add(alumno)
    session.commit()
    session.refresh(alumno)
    return alumno

def eliminar(session: Session, alumno_id: int) -> bool:
    """Eliminar un alumno"""
    alumno = obtener(session, alumno_id)  # Verificar que existe
    
    session.delete(alumno)
    session.commit()
    return True
