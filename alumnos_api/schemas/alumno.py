from pydantic import BaseModel, Field, validator

def _nota_field():
    return Field(..., ge=0.0, le=10.0, description="Rango 0.0 a 10.0")

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
