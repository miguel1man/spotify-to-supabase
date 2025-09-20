from fastapi import FastAPI
from src.presentation.api.v1 import auth, tracks
import logging

# Configuración básica de logging
logging.basicConfig(
    level=logging.DEBUG, # Cambiado a DEBUG para ver más detalles
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title="Spotify to Supabase Sync",
    description="API para sincronizar datos de Spotify a Supabase.",
    version="0.1.0",
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(tracks.router, prefix="/api/v1/tracks", tags=["Tracks"])

@app.get("/")
def read_root():
    logging.info("Acceso a la ruta raíz.")
    return {"message": "Welcome to the Spotify to Supabase Sync API"}
