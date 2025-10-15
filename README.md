# 📚 CRUD de Alumnos — FastAPI + MySQL + Frontend Vanilla JS

Proyecto completo de ejemplo que implementa un **CRUD de alumnos** usando:

- ⚙️ **Backend:** [FastAPI](https://fastapi.tiangolo.com/) + [PyMySQL](https://pymysql.readthedocs.io)
- 🗄️ **Base de datos:** MySQL
- 💻 **Frontend:** HTML, CSS y JavaScript vanilla
- 🌐 **CORS habilitado:** compatible con React, Vite o cualquier cliente web moderno

---

## 🚀 Características

- API REST con endpoints CRUD (`GET`, `POST`, `PUT`, `DELETE`)
- Validación de rango de notas (0.0 a 10.0)
- Cálculo automático del promedio final:  
  `promedioFinal = ((nota1 + nota2 + nota3)/3)*0.7 + notaFinal*0.3`
- Health check de base de datos (`/health/db`)
- CORS configurado para `localhost:3000` y `localhost:5173`
- Frontend minimalista y funcional con tabla dinámica, formulario y estilo moderno

---

## 🧩 Estructura del proyecto

```
CRUD-Alumnos/
│
├── backend/
│   └── main.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
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
En la carpeta `backend/`, ejecuta:

```bash
pip install "fastapi[all]" uvicorn black python-dotenv pymysql pydantic
```

### 2️⃣ Configurar conexión a MySQL
Edita las variables al inicio de `main.py`:

```python
DB_HOST = "192.168.1.251"
DB_PORT = 3306
DB_USER = xxxxxx
DB_PASSWORD = xxxxxx
DB_NAME = "crud_alumnos"
```

### 3️⃣ Ejecutar la API CMD
```bash
.venv\Scripts\activate
uvicorn main:app --reload
```

### 3️⃣ Ejecutar la API pcshell
```bash
.\.venv\Scripts\activate
uvicorn main:app --reload
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
| Backend | FastAPI |
| Base de datos | MySQL 8 |
| ORM / Conector | PyMySQL |
| Frontend | HTML5, CSS3, JavaScript (ES6) |
| Servidor | Uvicorn |

---

## 🧑‍💻 Autor

**Juan Carlos Sulbarán González**  
📧 sulbaranjc@gmail.com  
📍 Madrid, España  

> Proyecto educativo para enseñanza de programación y bases de datos.  
> Licencia MIT — libre uso y adaptación.
