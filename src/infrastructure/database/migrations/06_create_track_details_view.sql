-- 6. Vista de Detalles de Canciones
-- Proporciona una vista legible que une canciones, artistas y álbumes.
CREATE OR REPLACE VIEW public.track_details AS
SELECT
    t.id AS track_id,
    t.track_name,
    t.spotify_url,
    al.name AS album_name,
    -- Agrega los nombres de los artistas en una sola cadena, separados por comas
    string_agg(ar.name, ', ') AS artists_names
FROM
    public.spotify_tracks t
LEFT JOIN
    public.spotify_albums al ON t.album_id = al.id
LEFT JOIN
    public.spotify_track_artists ta ON t.id = ta.track_id
LEFT JOIN
    public.spotify_artists ar ON ta.artist_id = ar.id
GROUP BY
    t.id, al.id;

-- Es necesario conceder permisos sobre la vista
-- La RLS de las tablas subyacentes se aplica igualmente
GRANT SELECT ON public.track_details TO service_role;
