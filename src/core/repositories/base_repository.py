# src/core/repositories/base_repository.py
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Any
from uuid import UUID

# T es un marcador de tipo genérico para nuestras entidades (e.g., SavedTrack, Artist)
T = TypeVar('T')

class BaseRepository(Generic[T], ABC):
    """
    Interfaz base abstracta para operaciones CRUD genéricas.
    Define el contrato que cualquier repositorio de persistencia debe seguir.
    """

    @abstractmethod
    def create(self, entity: T) -> T:
        """Crea una nueva entidad en la base de datos."""
        pass

    @abstractmethod
    def get_by_id(self, entity_id: UUID) -> Optional[T]:
        """Obtiene una entidad por su ID."""
        pass

    @abstractmethod
    def get_by_spotify_id(self, spotify_id: str) -> Optional[T]:
        """Obtiene una entidad por su ID de Spotify."""
        pass

    @abstractmethod
    def get_all(self, limit: int = 100, offset: int = 0) -> List[T]:
        """Obtiene una lista de todas las entidades."""
        pass

    @abstractmethod
    def update(self, entity_id: UUID, updated_data: dict) -> Optional[T]:
        """Actualiza una entidad existente."""
        pass

    @abstractmethod
    def delete(self, entity_id: UUID) -> bool:
        """Elimina una entidad por su ID."""
        pass

    @abstractmethod
    def create_many(self, entities: List[T]) -> List[T]:
        """Crea múltiples entidades en la base de datos."""
        pass
