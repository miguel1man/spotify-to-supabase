# Spotify to Supabase Sync

Este proyecto es una API construida con FastAPI que sincroniza las canciones guardadas de un usuario de Spotify con una base de datos de Supabase.

## 🚀 Quick Start

1.  **Clonar el proyecto**:

    ```bash
    git clone https://github.com/miguel1man/spotify-to-supabase.git
    cd spotify-to-supabase
    ```

2.  **Instalar dependencias con `uv`**:

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    uv sync
    ```

3.  **Configurar credenciales**:
    Copia `.env.example` a `.env` y añade tus credenciales de Spotify y Supabase ([docs/SETUP.md](./docs/SETUP.md)).

    ```bash
    cp .env.example .env
    ```

4.  **Activar entorno y ejecutar la API**:

    ```bash
    source .venv/bin/activate
    uvicorn main:app --reload
    ```

5.  **Acceder a la documentación**: Abre tu navegador y ve a `http://127.0.0.1:8000/docs`.

## 🏗️ Arquitectura

El proyecto sigue una Arquitectura Hexagonal para una clara separación de responsabilidades. Para más detalles, consulta [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md).

## 🛠️ Configuración Detallada

Para una guía completa sobre la configuración del entorno, variables y dependencias, consulta [docs/SETUP.md](./docs/SETUP.md).

## 📝 Referencia de la API

La descripción de los endpoints, modelos de datos y esquemas de la base de datos se encuentra en [docs/API_REFERENCE.md](./docs/API_REFERENCE.md).
