import logging
from typing import Type, TypeVar, List, Optional, Generic
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, HttpUrl
from supabase import Client

from src.core.repositories.base_repository import BaseRepository

# Configuración del logger
logger = logging.getLogger(__name__)

# Marcador de tipo para las entidades Pydantic
EntityType = TypeVar('EntityType', bound=BaseModel)

class SupabaseRepository(BaseRepository[EntityType], Generic[EntityType]):
    """
    Implementación concreta y genérica de un repositorio para Supabase.
    Puede manejar operaciones CRUD para cualquier entidad Pydantic.
    """
    def __init__(self, supabase_client: Client, model: Type[EntityType], table_name: str):
        self.client = supabase_client
        self.model = model
        self.table_name = table_name

    def _serialize_entity(self, entity: EntityType) -> dict:
        entity_dict = entity.model_dump(exclude_unset=True)
        for key, value in entity_dict.items():
            # Convert HttpUrl to string to avoid serialization issues
            if hasattr(value, '__class__') and 'HttpUrl' in str(type(value)):
                entity_dict[key] = str(value)
            # Convert UUID to string to avoid JSON serialization issues
            if isinstance(value, UUID):
                entity_dict[key] = str(value)
            # Convert datetime to ISO string to avoid JSON serialization issues
            if isinstance(value, datetime):
                entity_dict[key] = value.isoformat()

        # Special handling for SavedTrack
        if self.model.__name__ == 'SavedTrack':
            # Exclude nested objects not in table
            entity_dict.pop('artists', None)
            entity_dict.pop('album', None)
            # Rename spotify_id to spotify_track_id for tracks table
            if 'spotify_id' in entity_dict:
                entity_dict['spotify_track_id'] = entity_dict.pop('spotify_id')
            # Ensure album_id is included if present
        return entity_dict

    def create(self, entity: EntityType) -> EntityType:
        entity_dict = self._serialize_entity(entity)
        try:
            response = self.client.table(self.table_name).insert(entity_dict).execute()
            if response.data:
                # Special handling for SavedTrack due to nested objects not in table
                if self.model.__name__ == 'SavedTrack':
                    created_entity = entity.model_copy()
                    created_entity.id = UUID(response.data[0]['id'])
                    if 'created_at' in response.data[0]:
                        created_entity.created_at = datetime.fromisoformat(response.data[0]['created_at'])
                    if 'updated_at' in response.data[0]:
                        created_entity.updated_at = datetime.fromisoformat(response.data[0]['updated_at'])
                    return created_entity
                else:
                    return self.model.model_validate(response.data[0])
            logger.warning(f"No se recibieron datos al crear la entidad en '{self.table_name}'.")
            return None
        except Exception as e:
            logger.error(f"Error al crear entidad en '{self.table_name}': {e}")
            raise

    def get_by_id(self, entity_id: UUID) -> Optional[EntityType]:
        try:
            response = self.client.table(self.table_name).select("*").eq('id', str(entity_id)).execute()
            if response.data:
                return self.model.model_validate(response.data[0])
            return None
        except Exception as e:
            logger.error(f"Error al obtener por ID '{entity_id}' de '{self.table_name}': {e}")
            raise

    def get_by_spotify_id(self, spotify_id: str) -> Optional[EntityType]:
        try:
            # Use the correct column name based on the table
            column_name = 'spotify_track_id' if self.table_name == 'spotify_tracks' else 'spotify_id'
            response = self.client.table(self.table_name).select("*").eq(column_name, spotify_id).execute()
            if response.data:
                return self.model.model_validate(response.data[0])
            return None
        except Exception as e:
            logger.error(f"Error al obtener por Spotify ID '{spotify_id}' de '{self.table_name}': {e}")
            raise

    def get_all(self, limit: int = 100, offset: int = 0) -> List[EntityType]:
        try:
            response = self.client.table(self.table_name).select("*").limit(limit).offset(offset).execute()
            return [self.model.model_validate(item) for item in response.data]
        except Exception as e:
            logger.error(f"Error al obtener todos los registros de '{self.table_name}': {e}")
            raise

    def update(self, entity_id: UUID, updated_data: dict) -> Optional[EntityType]:
        try:
            response = self.client.table(self.table_name).update(updated_data).eq('id', str(entity_id)).execute()
            if response.data:
                return self.model.model_validate(response.data[0])
            return None
        except Exception as e:
            logger.error(f"Error al actualizar entidad con ID '{entity_id}' en '{self.table_name}': {e}")
            raise

    def delete(self, entity_id: UUID) -> bool:
        try:
            response = self.client.table(self.table_name).delete().eq('id', str(entity_id)).execute()
            return bool(response.data)
        except Exception as e:
            logger.error(f"Error al eliminar entidad con ID '{entity_id}' en '{self.table_name}': {e}")
            raise

    def create_many(self, entities: List[EntityType]) -> List[EntityType]:
        entity_dicts = [self._serialize_entity(e) for e in entities]
        if not entity_dicts:
            return []
        try:
            response = self.client.table(self.table_name).insert(entity_dicts).execute()
            if response.data:
                # Special handling for SavedTrack due to nested objects not in table
                if self.model.__name__ == 'SavedTrack':
                    created_entities = []
                    for i, item in enumerate(response.data):
                        created_entity = entities[i].model_copy()
                        created_entity.id = UUID(item['id'])
                        if 'created_at' in item:
                            created_entity.created_at = datetime.fromisoformat(item['created_at'])
                        if 'updated_at' in item:
                            created_entity.updated_at = datetime.fromisoformat(item['updated_at'])
                        created_entities.append(created_entity)
                    return created_entities
                else:
                    return [self.model.model_validate(item) for item in response.data]
            logger.warning(f"No se recibieron datos al crear múltiples entidades en '{self.table_name}'.")
            return []
        except Exception as e:
            logger.error(f"Error al crear múltiples entidades en '{self.table_name}': {e}")
            raise