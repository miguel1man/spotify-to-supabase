from fastapi import Depends, HTTPException, status
from src.core.repositories.spotify_repository import SpotifyRepository
from src.adapters.spotify.repository import SpotifyAPIRepository
from src.core.services.sync_service import SyncService
from src.core.services.supabase_sync_service import SupabaseSyncService
from src.adapters.spotify import auth
from src.adapters.supabase.client import get_supabase_client
from src.adapters.supabase.repository import SupabaseRepository
from src.core.entities.track import Artist, Album, SavedTrack

def get_spotify_repository() -> SpotifyRepository:
    return SpotifyAPIRepository()

def get_sync_service(
    repo: SpotifyRepository = Depends(get_spotify_repository)
) -> SyncService:
    return SyncService(repo)

def get_spotify_token() -> str:
    """
    Esta función es una dependencia de FastAPI.
    Se encarga de obtener el token de acceso que fue guardado en memoria.

    Si el token no existe, lanza un error 401 para proteger el endpoint,
    forzando al usuario a autenticarse primero.

    FastAPI se encarga de "inyectar" el resultado de esta función en cualquier
    endpoint que la declare.
    """
    token = auth.get_access_token()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado en Spotify. Por favor, ve a /api/v1/auth/login",
        )
    return token

def get_supabase_artist_repository() -> SupabaseRepository[Artist]:
    supabase_client = get_supabase_client()
    return SupabaseRepository(supabase_client, Artist, "spotify_artists")

def get_supabase_album_repository() -> SupabaseRepository[Album]:
    supabase_client = get_supabase_client()
    return SupabaseRepository(supabase_client, Album, "spotify_albums")

def get_supabase_track_repository() -> SupabaseRepository[SavedTrack]:
    supabase_client = get_supabase_client()
    return SupabaseRepository(supabase_client, SavedTrack, "spotify_tracks")

def get_supabase_sync_service(
    artist_repo: SupabaseRepository[Artist] = Depends(get_supabase_artist_repository),
    album_repo: SupabaseRepository[Album] = Depends(get_supabase_album_repository),
    track_repo: SupabaseRepository[SavedTrack] = Depends(get_supabase_track_repository),
) -> SupabaseSyncService:
    return SupabaseSyncService(artist_repo, album_repo, track_repo)