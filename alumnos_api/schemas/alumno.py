from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import validator

def _nota_field():
    return Field(..., ge=0.0, le=10.0, description="Rango 0.0 a 10.0")

# Modelo base para la tabla
class AlumnoBase(SQLModel):
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

# Modelo para la tabla de base de datos
class Alumno(AlumnoBase, table=True):
    __tablename__ = "alumnos"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    promedioFinal: float = Field(...)

# Modelo para input (sin ID ni promedio, se calculan automáticamente)
class AlumnoIn(AlumnoBase):
    pass

# Modelo para output (con ID y promedio calculado)
class AlumnoOut(AlumnoBase):
    id: int
    promedioFinal: float
