-- Script para migrar datos de spotify_artists a artists con logging

-- Actualizar registros existentes donde hay coincidencia por name
WITH updated AS (
    UPDATE artists 
    SET 
        spotify_id = sa.spotify_id,
        spotify_url = sa.spotify_url,
        updated_at = NOW()
    FROM spotify_artists sa
    WHERE LOWER(TRIM(artists.name)) = LOWER(TRIM(sa.name))
    RETURNING 1
)
SELECT 'Registros actualizados: ' || COUNT(*) FROM updated;

-- Insertar nuevos registros que no existen en artists
WITH inserted AS (
    INSERT INTO artists (name, spotify_id, spotify_url, created_at, updated_at)
    SELECT 
        sa.name,
        sa.spotify_id,
        sa.spotify_url,
        sa.created_at,
        NOW()
    FROM spotify_artists sa
    WHERE NOT EXISTS (
        SELECT 1 
        FROM artists a 
        WHERE LOWER(TRIM(a.name)) = LOWER(TRIM(sa.name))
    )
    RETURNING 1
)
SELECT 'Registros insertados: ' || COUNT(*) FROM inserted;