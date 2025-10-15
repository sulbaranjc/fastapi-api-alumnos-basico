from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from alumnos_api.core.config import settings
from alumnos_api.core.logging import setup_logging
from alumnos_api.core.db import create_db_and_tables
from alumnos_api.api.routers import alumnos, health

log = setup_logging()

def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version=settings.version)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(alumnos.router)
    
    # Crear tablas automáticamente al iniciar la aplicación
    @app.on_event("startup")
    def on_startup():
        log.info("🚀 Iniciando API de Alumnos...")
        log.info("📊 Inicializando tablas de base de datos...")
        create_db_and_tables()
        log.info("✅ Tablas inicializadas correctamente")
    
    return app

# Imprescindible para uvicorn alumnos_api.main:app
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("alumnos_api.main:app", host="0.0.0.0", port=8000, reload=True)


