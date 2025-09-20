# 🛠️ Configuración del Entorno y Dependencias

Esta guía cubre todos los pasos necesarios para configurar y ejecutar el proyecto.

## 🚀 Quick Start con `uv` (Recomendado)

Estos comandos te permitirán tener el servidor FastAPI funcionando en minutos.

1.  **Clonar el proyecto**:

    ```bash
    git clone https://github.com/miguel1man/spotify-to-supabase.git
    cd spotify-to-supabase
    ```

2.  **Instalar `uv`**:

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

3.  **Crear entorno virtual y sincronizar dependencias**:

    ```bash
    uv sync
    ```

4.  **Configurar credenciales**:
    Copia el archivo de ejemplo `.env.example` a un nuevo archivo llamado `.env` y rellena tus credenciales.

    ```bash
    cp .env.example .env
    ```

    Asegúrate de rellenar `SPOTIFY_CLIENT_ID` y `SPOTIFY_CLIENT_SECRET` en el archivo `.env`.

5.  **Activar el entorno virtual**:

    ```bash
    source .venv/bin/activate
    ```

6.  **Ejecutar el servidor**:
    ```bash
    uv run uvicorn main:app --reload --host 127.0.0.1 --port 8000
    ```

Ahora, la API estará disponible en `http://127.0.0.1:8000`. Puedes ver la documentación interactiva en `http://127.0.0.1:8000/docs`.

---

## 🔧 Gestión de Dependencias

Este proyecto utiliza [uv](https://github.com/astral-sh/uv) para una gestión de dependencias y entornos virtuales de alto rendimiento.

#### Instalación alternativa con `pip`

Si prefieres no usar `uv`, puedes seguir estos pasos:

```bash
# 1. Crear un entorno virtual
python3.12 -m venv .venv

# 2. Activar el entorno
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar el servidor
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## 🔑 Configuración de Credenciales

### Variables de Entorno

El archivo `.env` es crucial para la configuración.

```env
# Spotify API Credentials
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8000/api/v1/auth/callback
SPOTIFY_ACCESS_TOKEN= # Opcional, se obtiene automáticamente

# Supabase Configuration (Opcional por ahora)
SUPABASE_URL=
SUPABASE_KEY=
SUPABASE_SERVICE_KEY=

# Application Settings
APP_HOST=127.0.0.1
APP_PORT=8000
APP_DEBUG=true
```

### Configuración de Spotify

1.  Ve al [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) y crea una nueva aplicación.
2.  Añade la siguiente URL de redirección en la configuración de tu aplicación: `http://127.0.0.1:8000/api/v1/auth/callback`.
3.  Copia el `CLIENT_ID` y `CLIENT_SECRET` en tu archivo `.env`.
4.  El scope `user-library-read` se solicita automáticamente en el flujo de autenticación.
