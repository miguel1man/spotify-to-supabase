import httpx
from typing import List
from src.core.repositories.spotify_repository import SpotifyRepository

class SpotifyAPIRepository(SpotifyRepository):
    """
    Implementación del repositorio de Spotify que interactúa con la API de Spotify.
    """
    BASE_URL = "https://api.spotify.com/v1"

    async def get_saved_tracks(self, offset: int, limit: int, token: str) -> List[dict]:
        """Obtiene las canciones guardadas del usuario desde la API de Spotify."""
        headers = {"Authorization": f"Bearer {token}"}
        params = {"limit": limit, "offset": offset}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.BASE_URL}/me/tracks", headers=headers, params=params)
                response.raise_for_status()
                return response.json().get("items", [])
            except httpx.HTTPStatusError as e:
                print(f"Error al obtener las canciones de Spotify: {e.response.text}")
                return []
