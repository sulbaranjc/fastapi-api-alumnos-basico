# 📚 CRUD de Alumnos — FastAPI + SQLModel + MySQL

Proyecto completo de ejemplo que implementa un **CRUD de alumnos** usando:

- ⚙️ **Backend:** [FastAPI](https://fastapi.tiangolo.com/) + [SQLModel](https://sqlmodel.tiangolo.com/)
- 🗄️ **Base de datos:** MySQL con SQLAlchemy
- 💻 **Frontend:** HTML, CSS y JavaScript vanilla
- 🌐 **CORS habilitado:** compatible con React, Vite o cualquier cliente web moderno

---

## 🚀 Características

- API REST con endpoints CRUD (`GET`, `POST`, `PUT`, `DELETE`)
- **SQLModel ORM** para manejo type-safe de base de datos
- Validación de rango de notas (0.0 a 10.0)
- Cálculo automático del promedio final:  
  `promedioFinal = ((nota1 + nota2 + nota3)/3)*0.7 + notaFinal*0.3`
- **Creación automática de tablas** con SQLModel
- Health check de base de datos (`/health/db`)
- CORS configurado para desarrollo
- **Dependency Injection** para sesiones de base de datos

---

## 🧩 Estructura del proyecto

```
fastapi-api-alumnos-basico/
│
├── alumnos_api/
│   ├── main.py              # Punto de entrada con auto-init de tablas
│   ├── deps.py              # Dependencias de FastAPI (SessionDep)
│   ├── api/routers/
│   │   ├── alumnos.py       # CRUD endpoints con SQLModel
│   │   └── health.py        # Health checks
│   ├── core/
│   │   ├── config.py        # Configuración con Pydantic Settings
│   │   ├── db.py            # SQLAlchemy engine + Session factory
│   │   ├── init_db.py       # Script para inicializar tablas
│   │   └── logging.py       # Sistema de logging
│   ├── repositories/
│   │   └── alumnos_repo.py  # Lógica de datos con SQLModel queries
│   ├── services/
│   │   └── alumnos_service.py  # Cálculo de promedios
│   └── schemas/
│       └── alumno.py        # Modelos SQLModel (tabla + DTOs)
├── tests/
├── .env.example             # Configuración de ejemplo
├── requirements.txt         # Incluye SQLModel
└── README.md
```

---

## ⚙️ Requisitos previos

- Python 3.9+
- MySQL Server 8.x
- Node.js (opcional, solo si usas React/Vite)

---

## 🗄️ Script SQL de base de datos

Ejecuta este script en tu servidor MySQL (por consola, Workbench o phpMyAdmin):

```sql
DROP DATABASE IF EXISTS crud_alumnos;
CREATE DATABASE IF NOT EXISTS crud_alumnos;
USE crud_alumnos;

CREATE TABLE IF NOT EXISTS alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    nota1 DOUBLE NOT NULL,
    nota2 DOUBLE NOT NULL,
    nota3 DOUBLE NOT NULL,
    notaFinal DOUBLE NOT NULL,
    promedioFinal DOUBLE NOT NULL
);
```

---

## ⚙️ Configuración del Backend

### 1️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2️⃣ Configurar variables de entorno
Copia y configura el archivo `.env`:
```bash
cp .env.example .env
```

Edita `.env` con tus datos de MySQL:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=crud_alumnos
```

### 3️⃣ Crear base de datos
Ejecuta este script en MySQL:
```sql
CREATE DATABASE IF NOT EXISTS crud_alumnos;
```

> ✨ **Las tablas se crean automáticamente** gracias a SQLModel al iniciar la API.

### 4️⃣ Ejecutar la API
```bash
.venv\Scripts\activate  
uvicorn alumnos_api.main:app --reload
```
### 3️⃣ Ejecutar la API Pcshell
```bash
.\.venv\Scripts\Activate.ps1
uvicorn alumnos_api.main:app --reload

```

📍 Accede a:
- API root → http://127.0.0.1:8000/
- Documentación Swagger → http://127.0.0.1:8000/docs  
- Health check → http://127.0.0.1:8000/health/db

---

## 🌐 Frontend Vanilla

### 1️⃣ Abrir el proyecto
En la carpeta `frontend/`, abre el archivo `index.html` en el navegador  
(recomendado: usar la extensión **Live Server** de VS Code).

### 2️⃣ Interactuar con la API
Podrás:
- Crear nuevos alumnos
- Editar notas existentes
- Eliminar alumnos
- Buscar por nombre en tiempo real

🧮 El promedio final se calcula automáticamente en el servidor.

---

## 🔐 CORS (para React / Vite)

Si desarrollas un frontend con React o Vite, tu backend ya acepta peticiones desde:

```python
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]
```

Agrega más dominios si lo despliegas en producción.

---

## 🧠 Endpoints principales

| Método | Endpoint | Descripción |
|:-------|:----------|:-------------|
| `GET` | `/` | Prueba general de la API |
| `GET` | `/health/db` | Verifica conexión a MySQL |
| `GET` | `/alumnos` | Lista todos los alumnos |
| `GET` | `/alumnos/{id}` | Devuelve un alumno por ID |
| `POST` | `/alumnos` | Crea un nuevo alumno |
| `PUT` | `/alumnos/{id}` | Actualiza un alumno existente |
| `DELETE` | `/alumnos/{id}` | Elimina un alumno |

---

## 🧪 Pruebas rápidas con curl o Postman

**Crear alumno:**
```bash
curl -X POST http://127.0.0.1:8000/alumnos ^
  -H "Content-Type: application/json" ^
  -d "{"nombre":"Juan Carlos","nota1":9.0,"nota2":8.5,"nota3":9.0,"notaFinal":9.5}"
```

**Listar alumnos:**
```bash
curl http://127.0.0.1:8000/alumnos
```

---

## 🧰 Tecnologías utilizadas

| Componente | Tecnología |
|-------------|-------------|
| Backend | FastAPI + SQLModel |
| Base de datos | MySQL 8 + SQLAlchemy |
| ORM | SQLModel (Pydantic + SQLAlchemy) |
| Dependency Injection | FastAPI Depends |
| Frontend | HTML5, CSS3, JavaScript (ES6) |
| Servidor | Uvicorn |

---

## 🆕 Novedades con SQLModel

- **🎯 Type Safety:** Modelos tipados que funcionan tanto para API como BD
- **🔄 Auto-migrations:** Creación automática de tablas
- **💉 Dependency Injection:** Sesiones de BD mediante FastAPI Depends
- **🧪 Fácil testing:** Modelos compartidos entre tests y producción
- **📝 Menos código:** Un solo modelo para tabla, input y output
- **🚀 Mejor rendimiento:** Connection pooling con SQLAlchemy

---

## 🧑‍💻 Autor

**Juan Carlos Sulbarán González**  
📧 sulbaranjc@gmail.com  
📍 Madrid, España  

> Proyecto educativo para enseñanza de programación y bases de datos.  
> Licencia MIT — libre uso y adaptación.

{
  "username": "admin",
  "password": "admin123"
}

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc2MDc4NzM4N30.jbUUlRbY6YHKNLjrCv4X1k3DvEKxFf3ZnX3v1SG8Ncw
