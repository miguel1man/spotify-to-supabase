from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import Optional, List
from uuid import UUID

class Artist(BaseModel):
    """Entidad de dominio para un artista."""
    spotify_id: str
    name: str
    spotify_url: HttpUrl

class Album(BaseModel):
    """Entidad de dominio para un álbum."""
    spotify_id: str
    name: str
    release_date: str
    spotify_url: HttpUrl

class SavedTrack(BaseModel):
    """Entidad de dominio para una canción guardada."""
    id: Optional[UUID] = None
    spotify_track_id: str = Field(..., description="ID de la canción en Spotify")
    track_name: str
    artists: List[Artist]
    album: Album
    spotify_url: HttpUrl
    added_at: datetime = Field(..., description="Fecha en que se guardó en Spotify")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

