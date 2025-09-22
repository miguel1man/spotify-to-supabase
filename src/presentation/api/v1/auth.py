from fastapi import APIRouter
from pydantic import BaseModel
from src.adapters.spotify import auth
import logging

router = APIRouter()


class LoginResponse(BaseModel):
    auth_url: str


@router.get(
    "/login",
    summary="Paso 1: Iniciar autenticación con Spotify",
    response_model=LoginResponse,
)
def login():
    """
    **Este endpoint inicia el flujo de autenticación OAuth2 con Spotify.**

    Genera la URL de autorización de Spotify a la que el usuario debe ser redirigido.
    Desde la UI de Swagger, puedes ejecutar este endpoint y luego copiar la `auth_url` de la respuesta
    y pegarla en una nueva pestaña de tu navegador para autorizar la aplicación.

    Después de que apruebes los permisos, Spotify te redirigirá de vuelta al endpoint `/callback` de esta API.
    """
    auth_url = auth.get_auth_url()
    logging.info(f"Generada URL de autorización de Spotify: {auth_url}")
    return {"auth_url": auth_url}

@router.get("/callback", summary="Paso 2: Callback automático de Spotify")
def callback(code: str):
    """
    **Este endpoint es para uso exclusivo de Spotify y se llama automáticamente.**
    
    **No necesitas llamarlo manualmente ni usarlo desde la UI de Swagger.**

    Spotify redirige al usuario aquí después de una autorización exitosa.
    La API recibe un `code` de un solo uso, lo intercambia por un `access_token` y lo almacena en memoria para futuras peticiones.
    Si intentas usar un `code` que ya fue utilizado (por ejemplo, recargando la página o usándolo aquí manualmente),
    recibirás un error de `invalid_grant`.
    """
    logging.info("Recibido el código de autorización de Spotify. Intercambiando por token...")
    token_data = auth.exchange_code_for_token(code)
    if token_data:
        logging.info("Token de acceso obtenido y almacenado correctamente.")
        return {"status": "success", "message": "Autenticación completada. Ya puedes cerrar esta pestaña y volver a la documentación para usar los otros endpoints."}
    logging.error("No se pudo obtener el token de acceso de Spotify.")
    return {"status": "error", "message": "No se pudo obtener el token de acceso."}

@router.get("/status", summary="Paso 3: Verificar estado de autenticación")
def status():
    """
    Verifica si hay un token de acceso válido almacenado en la sesión del servidor.
    Útil para comprobar si necesitas iniciar sesión antes de llamar a endpoints protegidos.
    """
    token = auth.get_access_token()
    if token:
        logging.debug("Token de acceso encontrado.")
        return {"status": "authenticated"}
    logging.debug("No se encontró token de acceso.")
    return {"status": "not authenticated"}
