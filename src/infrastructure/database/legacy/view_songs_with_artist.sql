-- Crear la vista que muestra canciones con sus artistas concatenados
CREATE OR REPLACE VIEW songs_with_artists AS
SELECT 
    s.id as song_id,
    s.title as song_title,
    -- Concatenar todos los artistas de la canción separados por comas
    STRING_AGG(sa.artist_name, ', ' ORDER BY sa.artist_name) as artists,
    s.created_at,
    s.updated_at,
    s.spotify_track_id as spotify_id
FROM 
    songs s
    LEFT JOIN song_artists sa ON s.id = sa.song_id
GROUP BY 
    s.id, 
    s.title, 
    s.created_at, 
    s.updated_at, 
    s.spotify_track_id;

-- Habilitar Row Level Security en la vista
ALTER VIEW songs_with_artists SET (security_invoker = true);

-- Crear política para la vista (ajusta según tus necesidades de seguridad)
-- Opción 1: Permitir acceso público de lectura
CREATE POLICY "allow_read_songs_with_artists" ON songs
FOR SELECT USING (true);

-- DROP VIEW song_artists_legible;