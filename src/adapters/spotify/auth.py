import httpx
import base64
import json
import os
from urllib.parse import urlencode
from src.infrastructure.config.settings import settings
import logging

# Definimos la ruta del archivo que usaremos para persistir el token.
TOKEN_FILE = "token.json"

# Este diccionario actúa como nuestro caché en memoria para el token.
# Se carga una vez desde el archivo al iniciar.
_token_storage = {"access_token": None, "refresh_token": None}

def _save_token_to_file(token_data: dict):
    """Guarda el diccionario del token en un archivo JSON."""
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)
    logging.info(f"Token guardado exitosamente en {TOKEN_FILE}")

def _load_token_from_file() -> dict | None:
    """Carga el token desde el archivo JSON si existe."""
    if not os.path.exists(TOKEN_FILE):
        return None
    try:
        with open(TOKEN_FILE, "r") as f:
            token_data = json.load(f)
            logging.info(f"Token cargado exitosamente desde {TOKEN_FILE}")
            return token_data
    except (json.JSONDecodeError, FileNotFoundError):
        return None

def get_auth_url() -> str:
    """Construye la URL de autorización de Spotify."""
    scope = 'user-library-read'
    auth_params = {
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
        'scope': scope,
    }
    return f"https://accounts.spotify.com/authorize?{urlencode(auth_params)}"

def exchange_code_for_token(code: str) -> dict | None:
    """Intercambia un código de autorización por un token de acceso y lo guarda."""
    token_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.b64encode(f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
    }
    
    logging.debug(f"Enviando petición a Spotify para intercambiar el código. Datos: {data}")

    try:
        with httpx.Client() as client:
            response = client.post(token_url, headers=headers, data=data)
            response.raise_for_status()
            token_data = response.json()
            
            # Guardar el token en el archivo y en la caché en memoria.
            _save_token_to_file(token_data)
            _token_storage["access_token"] = token_data.get("access_token")
            _token_storage["refresh_token"] = token_data.get("refresh_token")

            logging.debug(f"Token almacenado en caché: {token_data.get('access_token')[:15]}...")
            return token_data
    except httpx.HTTPStatusError as e:
        logging.error(f"Error al intercambiar el código por el token: {e.response.text}")
        return None

def get_access_token() -> str | None:
    """Devuelve el token de acceso, cargándolo desde el archivo si es necesario."""
    # Si el token ya está en la caché de memoria, lo usamos.
    if _token_storage["access_token"]:
        return _token_storage["access_token"]
    
    # Si no, intentamos cargarlo desde el archivo.
    token_data = _load_token_from_file()
    if token_data and "access_token" in token_data:
        # Guardamos en la caché para futuras peticiones.
        _token_storage["access_token"] = token_data["access_token"]
        _token_storage["refresh_token"] = token_data.get("refresh_token")
        return _token_storage["access_token"]

    # Si no hay token en ningún lado, retornamos None.
    return None
