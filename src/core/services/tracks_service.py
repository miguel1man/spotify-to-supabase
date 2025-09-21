import logging
import uuid
from pydantic import HttpUrl

from src.adapters.supabase.client import get_supabase_client
from src.adapters.supabase.repository import SupabaseRepository
from src.core.entities.track import SavedTrack

logger = logging.getLogger(__name__)

class SupabaseTracksService:
    """
    Servicio para probar la funcionalidad CRUD del repositorio de Supabase
    con datos sintéticos.
    """
    def __init__(self):
        supabase_client = get_supabase_client()
        self.track_repo = SupabaseRepository(supabase_client, SavedTrack, "spotify_tracks")

    def run_store_track(self, track_to_store: SavedTrack):
        """
        Ejecuta una prueba completa de CRUD para las entidades.
        """
        logger.info("🚀 Iniciando prueba de CRUD en Supabase...")

        try:
            logger.info(f"Creando track: {track_to_store.track_name}")
            created_track = self.track_repo.create(track_to_store)
            
            if not created_track or not created_track.id:
                raise Exception("La creación del Track falló, no se recibió ID.")
            
            logger.info(f"✅ Track creado con ID: {created_track.id}")

        except Exception as e:
            logger.error(f"❌ La prueba de CRUD falló: {e}", exc_info=True)
        finally:
            logger.info("🏁 Prueba de CRUD en Supabase finalizada.")