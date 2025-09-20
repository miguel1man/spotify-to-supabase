from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import List

class ArtistResponse(BaseModel):
    """Schema de respuesta para un artista."""
    name: str
    spotify_id: str
    spotify_url: HttpUrl

class AlbumResponse(BaseModel):
    """Schema de respuesta para un album."""
    name: str
    spotify_id: str
    spotify_url: HttpUrl
    release_date: str

class SavedTrackResponse(BaseModel):
    """Schema de respuesta para una canción guardada."""
    added_at: datetime
    spotify_track_id: str
    track_name: str
    artists: List[ArtistResponse]
    album: AlbumResponse
    spotify_url: HttpUrl
