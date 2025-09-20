from abc import ABC, abstractmethod
from typing import List

class SpotifyRepository(ABC):
    """
    Interfaz para el repositorio de Spotify, definiendo los métodos para obtener datos.
    """

    @abstractmethod
    async def get_saved_tracks(self, offset: int, limit: int, token: str) -> List[dict]:
        """Obtiene las canciones guardadas del usuario."""
        pass
