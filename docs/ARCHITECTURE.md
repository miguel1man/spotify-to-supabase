# 🏗️ Arquitectura del Proyecto

Este proyecto implementa una **Arquitectura Hexagonal** (también conocida como Puertos y Adaptadores) para lograr una clara separación de responsabilidades y facilitar la mantenibilidad y las pruebas.

## Diagrama de Arquitectura

El código está organizado en capas con dependencias que apuntan hacia el interior, hacia el dominio del negocio.

```
+-----------------------------------------------------------------+
| Presentation (FastAPI Endpoints, Schemas)                       |
|-----------------------------------------------------------------|
|               ↓ Depends on (interfaces) ↓                       |
+-----------------------------------------------------------------+
| Core / Domain (Entities, Repositories Interfaces, Services)     |
|-----------------------------------------------------------------|
| ↑ Implements (interfaces) ↑   | ↑ Implements (interfaces) ↑     |
+-------------------------------+---------------------------------+
| Adapters (Spotify Client)     | Adapters (Supabase Client)      |
+-------------------------------+---------------------------------+
```

- **Core/Domain**: Es el corazón de la aplicación. Contiene la lógica de negocio pura y las entidades (`track`, `artist`). No depende de ningún framework o tecnología externa. Define *interfaces* (contratos) para los repositorios.
- **Adapters**: Son la implementación concreta de las interfaces definidas en el Core. Hay adaptadores para interactuar con servicios externos como la API de Spotify o la base de datos de Supabase. Si quisiéramos cambiar de Supabase a otro proveedor de base de datos, solo tendríamos que crear un nuevo adaptador sin modificar el Core.
- **Presentation**: Es la capa más externa, responsable de la interacción con el usuario (en este caso, a través de una API REST). Utiliza los servicios del Core para realizar acciones.

## 📂 Estructura Detallada de Directorios

```
project-root/
├── .env.example
├── .gitignore
├── README.md
├── pyproject.toml
├── requirements.txt
├── main.py
├── src/
│   ├── adapters/
│   │   ├── spotify/
│   │   │   ├── client.py       # Cliente HTTP para la API de Spotify
│   │   │   ├── auth.py         # Lógica de autenticación OAuth2
│   │   │   └── repository.py   # Implementación del Repositorio de Spotify
│   │   └── supabase/
│   │       ├── client.py       # Cliente para interactuar con Supabase
│   │       └── repository.py   # Implementación genérica de repositorios para Supabase
│   ├── core/
│   │   ├── entities/
│   │   │   └── track.py, artist.py, album.py # Entidades de dominio
│   │   ├── repositories/
│   │   │   ├── base_repository.py      # Interfaz base para CRUD
│   │   │   ├── spotify_repository.py   # Interfaz para el repositorio de Spotify
│   │   │   └── track_repository.py     # Interfaz para el repositorio de Tracks
│   │   └── services/
│   │       ├── sync_service.py         # Lógica de negocio para la sincronización
│   │       └── supabase_test_service.py # Servicio para pruebas de Supabase
│   ├── infrastructure/
│   │   ├── config/
│   │   │   └── settings.py     # Carga de configuración desde .env
│   │   ├── database/
│   │   │   └── migrations/     # Scripts SQL para la creación de tablas (e.g., 01_create_artists.sql)
│   │   └── security/
│   │       └── oauth.py        # Utilidades de seguridad y OAuth
│   └── presentation/
│       ├── api/v1/
│       │   ├── auth.py, tracks.py, artists.py # Routers y endpoints de FastAPI
│       │   └── deps.py         # Dependencias inyectables de FastAPI
│       └── schemas/
│           └── track_schemas.py, ... # Esquemas Pydantic para validación
├── docs/
│   ├── README.md, SETUP.md, ARCHITECTURE.md, ...
├── prompts/
│   ├── README.md, 01-setup/, 02-authentication/, ...
├── notebooks/
│   ├── README.md, 01-setup/, 02-authentication/, ...
└── tests/
    ├── unit/
    └── integration/
```

## 🧩 Conceptos Clave de la Arquitectura

### Interfaces de Repositorio (`/core/repositories/`)

Estos archivos son **contratos abstractos** que definen qué operaciones debe implementar un repositorio. Siguen el **Principio de Inversión de Dependencias (D de SOLID)**.

**Ejemplo (`base_repository.py`):**
```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from uuid import UUID

T = TypeVar('T')

class BaseRepository(Generic[T], ABC):
    """Interfaz base para operaciones CRUD genéricas."""
    @abstractmethod
    async def create(self, entity: T) -> T:
        pass

    @abstractmethod
    async def get_by_id(self, entity_id: UUID) -> Optional[T]:
        pass
```

**Beneficios:**
- **Testabilidad**: Permite crear *mocks* de los repositorios para probar los servicios de forma aislada.
- **Flexibilidad**: Podemos cambiar la base de datos (el adaptador) sin tocar la lógica de negocio (el core).
- **Separación de Responsabilidades**: El dominio no sabe nada sobre Supabase; solo conoce las operaciones que puede realizar.

### Inyección de Dependencias (`/presentation/api/v1/deps.py`)

Este archivo contiene funciones que actúan como **dependencias inyectables** en los endpoints de FastAPI. FastAPI se encarga de resolver y "inyectar" el resultado de estas funciones en las rutas que las declaran.

**Ejemplo (`deps.py`):**
```python
from fastapi import Depends
from core.repositories.track_repository import TrackRepository
from adapters.supabase.repository import SupabaseTrackRepository

def get_track_repository() -> TrackRepository:
    """
    Inyección de dependencia que retorna una instancia concreta
    del repositorio de tracks.
    """
    return SupabaseTrackRepository()
```

**Uso en un endpoint:**
```python
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/tracks")
async def list_tracks(
    repository: TrackRepository = Depends(get_track_repository)
):
    return await repository.get_all()
```
Esto desacopla los endpoints de las implementaciones concretas, facilitando los cambios y las pruebas.
