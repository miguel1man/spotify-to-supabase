from fastapi import APIRouter, Depends, Query
from typing import List
from datetime import datetime
from src.core.services.sync_service import SyncService
from src.core.services.supabase_sync_service import SupabaseSyncService
from src.presentation.api.v1 import deps
from src.presentation.schemas.track import AlbumResponse, ArtistResponse, SavedTrackResponse
from src.core.entities.track import Artist, Album, SavedTrack
import logging

router = APIRouter()

@router.get("/sync", summary="Obtener canciones guardadas de Spotify", response_model=List[SavedTrackResponse])
async def sync_saved_tracks(
    offset: int = Query(0, description="El índice del primer elemento a devolver.", ge=0),
    limit: int = Query(10, description="El número máximo de elementos a devolver (1-50).", ge=1, le=50),
    sync_service: SyncService = Depends(deps.get_sync_service),
    supabase_sync_service: SupabaseSyncService = Depends(deps.get_supabase_sync_service),
    token: str = Depends(deps.get_spotify_token),
) -> List[SavedTrackResponse]:
    """
    Obtiene una lista paginada de las canciones que el usuario ha guardado en su biblioteca de 'Me Gusta' en Spotify.
    
    **Requiere autenticación previa.**
    """
    logging.info(f"🔍 Obteniendo canciones guardadas de Spotify (offset={offset}, limit={limit})")
    spotify_tracks = await sync_service.get_saved_tracks(offset, limit, token)
    logging.info(f"✅ Se encontraron {len(spotify_tracks)} canciones en Spotify")

    response_tracks = []
    saved_tracks = []

    for i, item in enumerate(spotify_tracks, 1):
        track = item['track']
        logging.debug(f"Procesando track {i}/{len(spotify_tracks)}: {track['name']}")

        # Build response objects
        artists_response = [
            ArtistResponse(
                name=artist['name'],
                spotify_id=artist['id'],
                spotify_url=artist['external_urls']['spotify']
            ) for artist in track['artists']
        ]
        album_response = AlbumResponse(
            name=track['album']['name'],
            spotify_id=track['album']['id'],
            spotify_url=track['album']['external_urls']['spotify'],
            release_date=track['album']['release_date']
        )
        saved_track_response = SavedTrackResponse(
            added_at=item['added_at'],
            spotify_track_id=track['id'],
            track_name=track['name'],
            artists=artists_response,
            album=album_response,
            spotify_url=track['external_urls']['spotify']
        )
        response_tracks.append(saved_track_response)

        # Build SavedTrack entity for saving
        artists_entity = [
            Artist(
                spotify_id=artist['id'],
                name=artist['name'],
                spotify_url=artist['external_urls']['spotify']
            ) for artist in track['artists']
        ]
        album_entity = Album(
            spotify_id=track['album']['id'],
            name=track['album']['name'],
            release_date=track['album']['release_date'],
            spotify_url=track['album']['external_urls']['spotify']
        )
        saved_track_entity = SavedTrack(
            spotify_track_id=track['id'],
            track_name=track['name'],
            artists=artists_entity,
            album=album_entity,
            spotify_url=track['external_urls']['spotify'],
            added_at=datetime.fromisoformat(item['added_at'].replace('Z', '+00:00'))
        )
        saved_tracks.append(saved_track_entity)

    logging.info(f"📦 Preparados {len(saved_tracks)} tracks para guardar en Supabase")

    # Save to Supabase
    logging.info("💾 Iniciando guardado en Supabase...")
    supabase_sync_service.save_saved_tracks(saved_tracks)
    logging.info("✅ Proceso de sincronización completado exitosamente")

    return response_tracks
