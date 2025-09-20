from typing import List
from src.core.repositories.spotify_repository import SpotifyRepository

class SyncService:
    """
    Servicio para la sincronización de datos desde Spotify.
    """
    def __init__(self, spotify_repo: SpotifyRepository):
        self._spotify_repo = spotify_repo

    async def get_saved_tracks(self, offset: int, limit: int, token: str) -> List[dict]:
        """Obtiene las canciones guardadas de Spotify."""
        return await self._spotify_repo.get_saved_tracks(offset, limit, token)
