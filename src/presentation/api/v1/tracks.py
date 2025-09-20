from fastapi import APIRouter, Depends, Query
from typing import List
from src.core.services.sync_service import SyncService
from src.presentation.api.v1 import deps
from src.presentation.schemas.track import AlbumResponse, ArtistResponse, SavedTrackResponse
import logging

router = APIRouter()

@router.get("/sync", summary="Obtener canciones guardadas de Spotify", response_model=List[SavedTrackResponse])
async def sync_saved_tracks(
    offset: int = Query(0, description="El índice del primer elemento a devolver.", ge=0),
    limit: int = Query(10, description="El número máximo de elementos a devolver (1-50).", ge=1, le=50),
    sync_service: SyncService = Depends(deps.get_sync_service),
    token: str = Depends(deps.get_spotify_token),
) -> List[SavedTrackResponse]:
    """
    Obtiene una lista paginada de las canciones que el usuario ha guardado en su biblioteca de 'Me Gusta' en Spotify.
    
    **Requiere autenticación previa.**
    """
    logging.info(f"Iniciando la obtención de canciones guardadas con offset={offset} y limit={limit}")
    spotify_tracks = await sync_service.get_saved_tracks(offset, limit, token)
    logging.info(f"Se encontraron {len(spotify_tracks)} canciones.")
    
    response_tracks = []
    for item in spotify_tracks:
        track = item['track']
        artists = [
            ArtistResponse(
                name=artist['name'],
                spotify_id=artist['id'],
                spotify_url=artist['external_urls']['spotify']
            ) for artist in track['artists']
        ]
        album = AlbumResponse(
            name=track['album']['name'],
            spotify_id=track['album']['id'],
            spotify_url=track['album']['external_urls']['spotify'],
            release_date=track['album']['release_date']
        )
        saved_track = SavedTrackResponse(
            added_at=item['added_at'],
            spotify_track_id=track['id'],
            track_name=track['name'],
            artists=artists,
            album=album,
            spotify_url=track['external_urls']['spotify']
        )
        response_tracks.append(saved_track)
        
    return response_tracks