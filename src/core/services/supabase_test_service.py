import logging
import uuid
from pydantic import HttpUrl

from src.adapters.supabase.client import get_supabase_client
from src.adapters.supabase.repository import SupabaseRepository
from src.core.entities.track import Artist

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabaseTestService:
    """
    Servicio para probar la funcionalidad CRUD del repositorio de Supabase
    con datos sintéticos.
    """
    def __init__(self):
        supabase_client = get_supabase_client()
        self.artist_repo = SupabaseRepository(supabase_client, Artist, "spotify_artists")

    def run_test(self):
        """
        Ejecuta una prueba completa de CRUD para las entidades.
        """
        logger.info("🚀 Iniciando prueba de CRUD en Supabase...")

        try:
            logger.info("--- Probando entidad Artist ---")
            
            synthetic_artist = Artist(
                spotify_id=f"artist_spotify_id_{uuid.uuid4()}",
                name=f"Artista de Prueba {uuid.uuid4()}",
                spotify_url=HttpUrl(f"https://open.spotify.com/artist/{uuid.uuid4()}")
            )
            logger.info(f"Creando artista: {synthetic_artist.name}")
            created_artist = self.artist_repo.create(synthetic_artist)
            
            if not created_artist or not created_artist.id:
                raise Exception("La creación del artista falló, no se recibió ID.")
            
            logger.info(f"✅ Artista creado con ID: {created_artist.id}")

            logger.info(f"Leyendo artista con ID: {created_artist.id}")
            retrieved_artist = self.artist_repo.get_by_id(created_artist.id)
            if not retrieved_artist:
                raise Exception("La lectura del artista falló.")
            logger.info(f"✅ Artista leído: {retrieved_artist.name}")
            assert retrieved_artist.name == synthetic_artist.name

            logger.info(f"Eliminando artista con ID: {created_artist.id}")
            deleted = self.artist_repo.delete(created_artist.id)
            if not deleted:
                raise Exception("La eliminación del artista falló.")
            logger.info("✅ Artista eliminado correctamente.")
            
            deleted_artist = self.artist_repo.get_by_id(created_artist.id)
            assert deleted_artist is None
            logger.info("✅ Verificación de eliminación exitosa.")

            logger.info("--- Prueba de entidad Artist completada con éxito ---")

        except Exception as e:
            logger.error(f"❌ La prueba de CRUD falló: {e}", exc_info=True)
        finally:
            logger.info("🏁 Prueba de CRUD en Supabase finalizada.")