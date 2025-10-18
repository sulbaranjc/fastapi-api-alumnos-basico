from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from alumnos_api.core.config import settings
from alumnos_api.core.logging import setup_logging
from alumnos_api.core.db import create_db_and_tables
from alumnos_api.api.routers import alumnos, health
from alumnos_api.api.routers import auth  # 👈 nuevo import
from fastapi.openapi.utils import get_openapi

log = setup_logging()

def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version=settings.version, debug=True)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(alumnos.router)
    app.include_router(auth.router)  # 👈 nuevo router
    
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

# ✅ Versión corregida del custom_openapi
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.app_name,
        version=settings.version,
        description="API CRUD protegida con JWT",
        routes=app.routes,
    )

    # Declaramos el esquema de seguridad para JWT
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # ✅ Eliminamos el bucle que añadía seguridad global a todos los endpoints
    # De esta manera, solo los endpoints que usen Depends(JWTBearer())
    # se mostrarán con candado 🔒 en Swagger UI

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("alumnos_api.main:app", host="0.0.0.0", port=8000, reload=True)
