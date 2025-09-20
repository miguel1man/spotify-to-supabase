# 📝 Referencia de API y Modelos de Datos

Este documento detalla los esquemas de la base de datos, los modelos Pydantic y los endpoints de la API REST.

## 🚀 Endpoints de la API (`/api/v1/`)

### Autenticación

- `GET /api/v1/auth/login`: Redirige al usuario a la página de autorización de Spotify para iniciar el flujo OAuth2.
- `GET /api/v1/auth/callback`: Endpoint de callback que Spotify utiliza para devolver el código de autorización. Intercambia el código por un token de acceso y lo almacena en la sesión del servidor.
- `GET /api/v1/auth/status`: Verifica si el usuario está actualmente autenticado (es decir, si hay un token de acceso en la sesión).

### Sincronización

- `GET /api/v1/tracks/sync`: Obtiene un lote de canciones guardadas de Spotify. Requiere que el usuario esté autenticado.
  - **Query Parameters**:
    - `offset` (int, opcional, default: 0): El índice del primer elemento a devolver.
    - `limit` (int, opcional, default: 10): El número máximo de elementos a devolver (entre 1 y 50).

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
