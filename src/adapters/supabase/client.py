from supabase import create_client, Client
from src.infrastructure.config.settings import settings

# Crear una única instancia del cliente de Supabase
supabase_client: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_KEY
)

def get_supabase_client() -> Client:
    """
    Retorna la instancia del cliente de Supabase.
    """
    return supabase_client