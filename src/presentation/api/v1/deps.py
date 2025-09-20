from fastapi import Depends, HTTPException, status
from src.core.repositories.spotify_repository import SpotifyRepository
from src.adapters.spotify.repository import SpotifyAPIRepository
from src.core.services.sync_service import SyncService
from src.adapters.spotify import auth

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