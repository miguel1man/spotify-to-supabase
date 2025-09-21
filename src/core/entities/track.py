from pydantic import BaseModel, Field, HttpUrl, field_serializer
from datetime import datetime
from typing import Optional, List
from uuid import UUID

class Artist(BaseModel):
    """Entidad de dominio para un artista."""
    id: Optional[UUID] = None
    spotify_id: str
    name: str
    spotify_url: HttpUrl

    @field_serializer('spotify_url')
    def serialize_url(self, url: HttpUrl, _info):
        return str(url)

class Album(BaseModel):
    """Entidad de dominio para un álbum."""
    id: Optional[UUID] = None
    spotify_id: str
    name: str
    release_date: str
    spotify_url: HttpUrl
    album_type: Optional[str] = None
    artists: List[Artist] = []

    @field_serializer('spotify_url')
    def serialize_url(self, url: HttpUrl, _info):
        return str(url)

class SavedTrack(BaseModel):
    """Entidad de dominio para una canción guardada."""
    id: Optional[UUID] = None
    spotify_track_id: str = Field(..., description="ID de la canción en Spotify")
    track_name: str
    artists: List[Artist]
    album: Optional[Album] = None
    album_id: Optional[UUID] = None
    spotify_url: HttpUrl
    added_at: datetime = Field(..., description="Fecha en que se guardó en Spotify")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_serializer('spotify_url')
    def serialize_url(self, url: HttpUrl, _info):
        return str(url)

