# 🛠️ Configuración del Entorno y Dependencias

Esta guía cubre todos los pasos necesarios para configurar el entorno de desarrollo local.

## 💻 Stack Tecnológico

- **Backend**: Python 3.12 con FastAPI
- **Entorno**: WSL (Windows Subsystem for Linux)
- **Gestor de dependencias**: uv (de Astral)
- **Base de datos**: Supabase (PostgreSQL)
- **Autenticación**: Spotify OAuth 2.0
- **Validación de Datos**: Pydantic v2
- **Cliente HTTP**: httpx

### Compatibilidad con Python 3.12

El proyecto está optimizado para Python 3.12, aprovechando características como:
- Sentencias `match-case` (disponibles desde Python 3.10).
- Mejoras en `dataclasses` y `typing`.
- `asyncio` mejorado.
- Uso de `pathlib` para un manejo de rutas agnóstico al sistema operativo.

## 🔧 Gestión de Dependencias

Este proyecto utiliza [uv](https://github.com/astral-sh/uv) para una gestión de dependencias y entornos virtuales de alto rendimiento.

#### Instalación con `uv` (Recomendado)
```bash
# 1. Instalar uv (si aún no lo has hecho)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clonar el proyecto
git clone <repository-url>
cd spotify-supabase-tracker

# 3. Crear el entorno virtual e instalar dependencias
uv sync

# 4. Activar el entorno virtual
source .venv/bin/activate
```

#### Instalación alternativa con `pip`
```bash
# 1. Crear un entorno virtual
python -m venv .venv

# 2. Activar el entorno
source .venv/bin/activate

# 3. Instalar dependencias desde requirements.txt
pip install -r requirements.txt
```

## 🔑 Configuración de Credenciales

### Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto, basándote en el archivo `.env.example`.

```env
# Spotify API Credentials
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8000/callback

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key

# Application Settings
APP_HOST=127.0.0.1
APP_PORT=8000
APP_DEBUG=true
```

### Configuración de Spotify
1.  Ve al [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) y crea una nueva aplicación.
2.  Añade la siguiente URL de redirección en la configuración de tu aplicación: `http://127.0.0.1:8000/callback`.
3.  Copia el `CLIENT_ID` y `CLIENT_SECRET` en tu archivo `.env`.
4.  Asegúrate de que tu aplicación de Spotify solicita el scope `user-library-read`.

### Configuración de Supabase
1.  Crea un nuevo proyecto en [Supabase](https://supabase.com).
2.  En la configuración del proyecto, ve a la sección de "API".
3.  Copia la URL del proyecto, la `anon key` y la `service_role key` en tu archivo `.env`.
4.  Ejecuta las migraciones SQL (disponibles en [API Reference](./API_REFERENCE.md#modelo-de-datos)) en el "SQL Editor" de Supabase para crear las tablas necesarias.

## 🚦 Comandos de Desarrollo

### Con `uv` (Recomendado)
```bash
# Instalar/sincronizar dependencias
uv sync

# Activar entorno virtual
source .venv/bin/activate

# Ejecutar servidor de desarrollo con recarga automática
uv run uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Ejecutar tests
uv run pytest

# Abrir Jupyter Notebooks
uv run jupyter lab notebooks/

# Formatear código
uv run black src/
uv run isort src/

# Análisis estático y linting
uv run flake8 src/
uv run mypy src/
```

### Con `pip` (Alternativo)
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor de desarrollo
uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Ejecutar tests
pytest
```

La documentación automática de la API estará disponible en:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`
