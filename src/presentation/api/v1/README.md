# README: API v1

Esta API permite interactuar con los datos de Spotify y Supabase.

## Flujo de Autenticación: Del Código al Token

La API utiliza el flujo de **OAuth2 Authorization Code** de Spotify. Es un proceso de varios pasos diseñado para ser seguro, pero puede ser confuso al probarlo desde una herramienta como Swagger. Aquí te lo explicamos en detalle.

### Paso 1: Iniciar el Proceso (`/auth/login`)

El flujo comienza cuando navegas a este endpoint en tu navegador (no desde Swagger).

- **Qué hace la API**: Genera una URL especial de Spotify y te redirige a ella.
- **Tu acción**: Abre `http://127.0.0.1:8000/api/v1/auth/login` en una nueva pestaña. Verás la página de inicio de sesión de Spotify.

### Paso 2: Autorización en Spotify

- **Qué haces tú**: Inicias sesión en Spotify y aceptas los permisos que la aplicación solicita.
- **Qué hace Spotify**: Si todo es correcto, Spotify genera un **código de autorización (`code`)** y redirige tu navegador de vuelta a la `redirect_uri` que configuramos: `http://127.0.0.1:8000/api/v1/auth/callback?code=...`.

### Paso 3: El Callback Mágico (`/auth/callback`)

Este es el paso más importante y el que causa la confusión.

- **Qué hace tu navegador**: Inmediatamente después de ser redirigido por Spotify, tu navegador hace una petición `GET` a `/api/v1/auth/callback` con el `code` en la URL.
- **Qué hace la API**: 
    1. Recibe la petición con el `code`.
    2. Realiza una petición segura de servidor a servidor hacia la API de Spotify para intercambiar ese `code` por un **`access_token`** y un **`refresh_token`**.
    3. **Almacena el token**: El `access_token` se guarda en un archivo `token.json` en la raíz del proyecto. Este archivo está incluido en `.gitignore` por seguridad.
    4. Responde a tu navegador con un mensaje de éxito.

> **¡ADVERTENCIA!** El `code` de autorización es de **un solo uso**. Si intentas llamar manualmente al endpoint `/callback` con un código que tu navegador ya usó, Spotify devolverá el error `invalid_grant`, porque ese código ya fue consumido.

### Paso 4: Usar la API (`/tracks/sync`)

Ahora que la API tiene el token almacenado en `token.json`, puedes llamar a otros endpoints. El token persistirá incluso si reinicias el servidor.

## ¿Cómo se consume el token almacenado?

La "magia" de cómo los endpoints obtienen el token sin que tengas que pasarlo manualmente se llama **Inyección de Dependencias**, una característica clave de FastAPI.

1.  **Se define una dependencia**: En `src/presentation/api/v1/deps.py`, hay una función llamada `get_spotify_token`.

    ```python
    # src/presentation/api/v1/deps.py

    def get_spotify_token() -> str:
        """
        Esta función obtiene el token. Primero lo busca en la caché en memoria,
        y si no está, lo carga desde el archivo `token.json`.
        Si no lo encuentra en ningún lado, falla con un error 401.
        """
        token = auth.get_access_token() # Lee de la caché/archivo
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No autenticado...",
            )
        return token
    ```

2.  **El endpoint declara la dependencia**: El endpoint `/tracks/sync` le dice a FastAPI que "depende" de `get_spotify_token`.

    ```python
    # src/presentation/api/v1/tracks.py

    @router.get("/sync")
    async def sync_saved_tracks(
        ...,
        token: str = Depends(deps.get_spotify_token), # <--- ¡AQUÍ!
    ):
        # ...
    ```

3.  **FastAPI hace el trabajo**: Antes de ejecutar el código de `sync_saved_tracks`, FastAPI ejecuta `get_spotify_token`, toma el `token` que esta retorna y lo pasa como un parámetro a `sync_saved_tracks`. Es automático y asegura que solo el código autenticado pueda ejecutar el endpoint.

## Resumen del Flujo de Token

1.  **`Authorization Code`**: Temporal y de un solo uso. Sirve para demostrar que el usuario te ha autorizado.
2.  **`Access Token`**: La "llave" para la API de Spotify. Se almacena en `token.json` y se reutiliza automáticamente gracias a la inyección de dependencias.
3.  **`Refresh Token`**: De larga duración. Se puede usar para obtener un nuevo `access_token` cuando el actual expire. (La lógica de refresco aún no está implementada).