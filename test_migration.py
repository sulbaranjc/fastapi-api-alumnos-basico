"""
Script de test para verificar la migración a SQLModel
"""
import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alumnos_api.core.db import engine, create_db_and_tables
from alumnos_api.schemas.alumno import Alumno, AlumnoIn
from sqlmodel import Session

def test_sqlmodel_migration():
    """Test básico para verificar que SQLModel funciona correctamente"""
    
    print("🧪 Iniciando test de migración a SQLModel...")
    
    # 1. Crear tablas
    print("📊 Creando tablas...")
    create_db_and_tables()
    print("✅ Tablas creadas exitosamente")
    
    # 2. Test de inserción
    print("📝 Insertando alumno de prueba...")
    alumno_data = AlumnoIn(
        nombre="Juan Test",
        nota1=8.5,
        nota2=9.0,
        nota3=8.0,
        notaFinal=9.2
    )
    
    with Session(engine) as session:
        # Crear alumno
        promedio = ((alumno_data.nota1 + alumno_data.nota2 + alumno_data.nota3) / 3.0) * 0.7 + alumno_data.notaFinal * 0.3
        
        alumno = Alumno(
            nombre=alumno_data.nombre,
            nota1=alumno_data.nota1,
            nota2=alumno_data.nota2,
            nota3=alumno_data.nota3,
            notaFinal=alumno_data.notaFinal,
            promedioFinal=promedio
        )
        
        session.add(alumno)
        session.commit()
        session.refresh(alumno)
        
        print(f"✅ Alumno creado con ID: {alumno.id}")
        print(f"📊 Promedio calculado: {alumno.promedioFinal}")
    
    # 3. Test de consulta
    print("🔍 Consultando alumnos...")
    with Session(engine) as session:
        from sqlmodel import select
        statement = select(Alumno)
        alumnos = session.exec(statement).all()
        print(f"✅ Encontrados {len(alumnos)} alumnos en la base de datos")
        
        for alumno in alumnos:
            print(f"   - {alumno.nombre}: {alumno.promedioFinal}")
    
    print("🎉 ¡Migración a SQLModel completada exitosamente!")

if __name__ == "__main__":
    test_sqlmodel_migration()