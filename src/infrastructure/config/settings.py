from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Configuraciones de la aplicación, cargadas desde variables de entorno.
    """
    # Spotify
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_REDIRECT_URI: str
    SPOTIFY_ACCESS_TOKEN: Optional[str] = None

    # Supabase
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    SUPABASE_SERVICE_KEY: Optional[str] = None

    # Application
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    APP_DEBUG: bool = False


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()