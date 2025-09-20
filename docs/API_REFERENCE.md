# 📝 Referencia de API y Modelos de Datos

Este documento detalla los esquemas de la base de datos, los modelos Pydantic y los endpoints de la API REST.

## 📊 Modelo de Datos (SQL)

Las siguientes tablas deben ser creadas en Supabase a través del "SQL Editor".

### Tabla: `saved_tracks`
```sql
CREATE TABLE saved_tracks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    spotify_track_id VARCHAR(100) NOT NULL UNIQUE,
    track_name TEXT NOT NULL,
    artist_name TEXT NOT NULL,
    album_name TEXT NOT NULL,
    album_release_date DATE,
    spotify_url VARCHAR(200) NOT NULL,
    added_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para optimizar consultas
CREATE INDEX idx_saved_tracks_spotify_id ON saved_tracks(spotify_track_id);
CREATE INDEX idx_saved_tracks_artist ON saved_tracks(artist_name);
CREATE INDEX idx_saved_tracks_added_at ON saved_tracks(added_at);

-- Política de Seguridad a Nivel de Fila (RLS)
ALTER TABLE saved_tracks ENABLE ROW LEVEL SECURITY;

-- Política para permitir todas las operaciones a roles de servicio (service_role)
CREATE POLICY "service_role_policy" ON saved_tracks
FOR ALL
USING (auth.role() = 'service_role');
```

### Tabla: `artists`
```sql
CREATE TABLE artists (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    spotify_artist_id VARCHAR(100) NOT NULL UNIQUE,
    artist_name TEXT NOT NULL,
    spotify_url VARCHAR(200) NOT NULL,
    genres TEXT[],
    popularity INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Tabla: `albums`
```sql
CREATE TABLE albums (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    spotify_album_id VARCHAR(100) NOT NULL UNIQUE,
    album_name TEXT NOT NULL,
    artist_name TEXT NOT NULL,
    release_date DATE,
    spotify_url VARCHAR(200) NOT NULL,
    total_tracks INTEGER,
    album_type VARCHAR(50), -- e.g., album, single, compilation
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 📝 Modelos Pydantic

Estos modelos se utilizan para la validación de datos, la serialización y la documentación automática de la API.

### `SavedTrack` (Entidad de Dominio)
```python
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from uuid import UUID
from typing import Optional

class SavedTrack(BaseModel):
    """Entidad de dominio para una canción guardada."""
    id: UUID
    spotify_track_id: str = Field(..., description="ID de la canción en Spotify")
    track_name: str
    artist_name: str
    album_name: str
    album_release_date: Optional[datetime] = None
    spotify_url: str
    added_at: datetime = Field(..., description="Fecha en que se guardó en Spotify")
    created_at: datetime
    updated_at: datetime
```

### `Artist` (Entidad de Dominio)
```python
class Artist(BaseModel):
    """Entidad de dominio para un artista."""
    id: UUID
    spotify_artist_id: str
    artist_name: str
    spotify_url: str
    genres: Optional[list[str]] = None
    popularity: Optional[int] = None
    created_at: datetime
    updated_at: datetime
```

### `Album` (Entidad de Dominio)
```python
class Album(BaseModel):
    """Entidad de dominio para un álbum."""
    id: UUID
    spotify_album_id: str
    album_name: str
    artist_name: str
    release_date: Optional[datetime] = None
    spotify_url: str
    total_tracks: Optional[int] = None
    album_type: Optional[str] = None
    created_at: datetime
    updated_at: datetime
```

## 🚀 Endpoints de la API (`/api/v1/`)

### Autenticación
- `GET /auth/login`: Redirige al usuario a la página de autorización de Spotify para iniciar el flujo OAuth2.
- `GET /callback`: Endpoint de callback que Spotify utiliza para devolver el código de autorización.
- `GET /auth/status`: Verifica el estado de la autenticación actual.

### Sincronización
- `GET /tracks/sync`: Inicia una sincronización completa de todas las canciones guardadas desde Spotify a Supabase.
- `GET /tracks/sync/{offset}/{limit}`: Sincroniza un lote específico de canciones. Útil para grandes bibliotecas.
  - *Ejemplo*: `/api/v1/tracks/sync/50/50` sincroniza las siguientes 50 canciones a partir de la posición 50.

### Gestión de Canciones
- `GET /tracks`: Devuelve una lista paginada de canciones desde Supabase.
  - *Query params*: `offset: int = 0`, `limit: int = 20`.
- `GET /tracks/{track_id}`: Obtiene una canción específica por su ID de la base de datos.
- `DELETE /tracks/{track_id}`: Elimina una canción de la base de datos.

### Gestión de Artistas y Álbumes
- `GET /artists`: Devuelve una lista paginada de artistas.
- `GET /albums`: Devuelve una lista paginada de álbumes.
