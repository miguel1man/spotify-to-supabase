import logging
from typing import List
from src.adapters.supabase.repository import SupabaseRepository
from src.core.entities.track import Artist, Album, SavedTrack
from src.adapters.supabase.client import get_supabase_client

logger = logging.getLogger(__name__)

class SupabaseSyncService:
    """
    Servicio para sincronizar datos de Spotify a Supabase.
    Maneja la creación de artistas, álbumes y tracks con sus relaciones.
    """

    def __init__(
        self,
        artist_repo: SupabaseRepository[Artist],
        album_repo: SupabaseRepository[Album],
        track_repo: SupabaseRepository[SavedTrack],
    ):
        self.artist_repo = artist_repo
        self.album_repo = album_repo
        self.track_repo = track_repo
        self.client = get_supabase_client()

    def save_saved_tracks(self, tracks: List[SavedTrack]) -> List[SavedTrack]:
        """
        Guarda las tracks en Supabase, creando artistas y álbumes si no existen.
        Retorna las tracks guardadas.
        """
        logger.info(f"Iniciando guardado de {len(tracks)} tracks en Supabase")
        saved_tracks = []
        created_artists = 0
        created_albums = 0
        created_tracks = 0
        skipped_tracks = 0

        for i, track in enumerate(tracks, 1):
            try:
                logger.debug(f"Procesando track {i}/{len(tracks)}: {track.track_name}")

                # Guardar artistas
                saved_artists = []
                for artist in track.artists:
                    try:
                        existing_artist = self.artist_repo.get_by_spotify_id(artist.spotify_id)
                        if existing_artist:
                            saved_artists.append(existing_artist)
                            logger.debug(f"Artista existente encontrado: {artist.name}")
                        else:
                            saved_artist = self.artist_repo.create(artist)
                            saved_artists.append(saved_artist)
                            created_artists += 1
                            logger.info(f"✓ Artista creado: {saved_artist.name}")
                    except Exception as e:
                        logger.error(f"Error procesando artista {artist.name}: {e}")
                        raise

                # Guardar álbum
                try:
                    existing_album = self.album_repo.get_by_spotify_id(track.album.spotify_id)
                    if existing_album:
                        saved_album = existing_album
                        logger.debug(f"Álbum existente encontrado: {track.album.name}")
                    else:
                        saved_album = self.album_repo.create(track.album)
                        created_albums += 1
                        logger.info(f"✓ Álbum creado: {saved_album.name}")
                except Exception as e:
                    logger.error(f"Error procesando álbum {track.album.name}: {e}")
                    raise

                # Verificar si track ya existe
                existing_track = self.track_repo.get_by_spotify_id(track.spotify_track_id)
                if existing_track:
                    saved_tracks.append(existing_track)
                    skipped_tracks += 1
                    logger.debug(f"Track ya existe, omitiendo: {track.track_name}")
                    continue

                # Crear track con album_id
                track.album_id = saved_album.id
                saved_track = self.track_repo.create(track)
                created_tracks += 1
                logger.info(f"✓ Track creado: {saved_track.track_name}")

                # Guardar relaciones track-artists
                for artist in saved_artists:
                    try:
                        self.client.table("spotify_track_artists").insert({
                            "track_id": str(saved_track.id),
                            "artist_id": str(artist.id)
                        }).execute()
                        logger.debug(f"Relación creada: track {saved_track.track_name} - artist {artist.name}")
                    except Exception as e:
                        logger.warning(f"Relación track-artist ya existe o error: {e}")

                saved_tracks.append(saved_track)

            except Exception as e:
                logger.error(f"❌ Error guardando track '{track.track_name}' (ID: {track.spotify_track_id}): {str(e)}")
                logger.error(f"Detalles del error: {type(e).__name__}: {e}")
                continue

        logger.info("📊 Resumen del proceso de guardado:")
        logger.info(f"  • Tracks procesados: {len(tracks)}")
        logger.info(f"  • Tracks creados: {created_tracks}")
        logger.info(f"  • Tracks omitidos (ya existían): {skipped_tracks}")
        logger.info(f"  • Artistas creados: {created_artists}")
        logger.info(f"  • Álbumes creados: {created_albums}")
        logger.info(f"  • Total tracks guardados: {len(saved_tracks)}")

        return saved_tracks