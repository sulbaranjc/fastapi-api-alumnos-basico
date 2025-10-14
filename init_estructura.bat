@echo off
REM === Crear carpetas base ===
mkdir app 2>nul
mkdir app\api\routers 2>nul
mkdir app\core 2>nul
mkdir app\repositories 2>nul
mkdir app\services 2>nul
mkdir app\schemas 2>nul
mkdir tests 2>nul

REM === Crear archivos vacíos si no existen ===
type NUL > app\api\__init__.py
type NUL > app\api\routers\__init__.py
type NUL > app\core\__init__.py
type NUL > app\repositories\__init__.py
type NUL > app\services\__init__.py
type NUL > app\schemas\__init__.py
type NUL > app\deps.py
type NUL > app\main.py
type NUL > app\core\config.py
type NUL > app\core\db.py
type NUL > app\core\logging.py
type NUL > app\api\routers\health.py
type NUL > app\api\routers\alumnos.py
type NUL > app\schemas\alumno.py
type NUL > app\services\alumnos_service.py
type NUL > app\repositories\alumnos_repo.py
type NUL > tests\test_alumnos.py
echo Estructura creada.
