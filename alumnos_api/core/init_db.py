"""
Script para inicializar la base de datos con SQLModel
"""
from sqlmodel import SQLModel
from alumnos_api.core.db import engine
from alumnos_api.schemas.alumno import Alumno  # Importar para registrar el modelo

def init_db():
    """
    Crear todas las tablas en la base de datos
    """
    print("🔄 Creando tablas de base de datos...")
    SQLModel.metadata.create_all(engine)
    print("✅ Tablas creadas exitosamente!")

def drop_db():
    """
    Eliminar todas las tablas de la base de datos
    """
    print("🗑️ Eliminando tablas de base de datos...")
    SQLModel.metadata.drop_all(engine)
    print("✅ Tablas eliminadas exitosamente!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--drop":
        drop_db()
    else:
        init_db()