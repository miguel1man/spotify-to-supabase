-- Script mejorado para verificar migración de pares artista-canción únicos
WITH table_counts AS (
    SELECT 
        (SELECT COUNT(*) FROM spotify_artists) as spotify_artists_count,
        (SELECT COUNT(*) FROM spotify_albums) as spotify_albums_count,
        (SELECT COUNT(*) FROM spotify_tracks) as spotify_tracks_count,
        (SELECT COUNT(*) FROM spotify_album_artists) as spotify_album_artists_count,
        (SELECT COUNT(*) FROM spotify_track_artists) as spotify_track_artists_count,
        (SELECT COUNT(*) FROM songs) as songs_count,
        (SELECT COUNT(*) FROM artists) as artists_count,
        (SELECT COUNT(*) FROM song_artists) as song_artists_count,
        
        -- Coincidencias de artistas únicos
        (SELECT COUNT(*) 
         FROM spotify_artists sa 
         INNER JOIN artists a ON LOWER(TRIM(sa.name)) = LOWER(TRIM(a.name))
        ) as matching_artists_count,
        
        -- Coincidencias de canciones únicas
        (SELECT COUNT(*) 
         FROM spotify_tracks st 
         INNER JOIN songs s ON LOWER(TRIM(st.track_name)) = LOWER(TRIM(s.title))
        ) as matching_tracks_count,
        
        -- CORRECCIÓN: Contar pares únicos artista-canción que existen en ambas tablas
        (SELECT COUNT(*)
         FROM spotify_track_artists sta
         WHERE EXISTS (
             SELECT 1 
             FROM song_artists so 
             WHERE LOWER(TRIM(sta.spotify_track_name)) = LOWER(TRIM(so.song_title))
               AND LOWER(TRIM(sta.artist_name)) = LOWER(TRIM(so.artist_name))
         )
        ) as matching_unique_pairs_count,
        
        -- Pares de spotify que NO tienen coincidencia exacta en legacy
        (SELECT COUNT(*)
         FROM spotify_track_artists sta
         WHERE NOT EXISTS (
             SELECT 1 
             FROM song_artists so 
             WHERE LOWER(TRIM(sta.spotify_track_name)) = LOWER(TRIM(so.song_title))
               AND LOWER(TRIM(sta.artist_name)) = LOWER(TRIM(so.artist_name))
         )
        ) as missing_pairs_count
)
SELECT 
    'Artistas legacy' as descripcion,
    artists_count as cantidad,
    '' as porcentaje,
    1 as orden
FROM table_counts
UNION ALL
SELECT 
    'Artistas spotify' as descripcion,
    spotify_artists_count as cantidad,
    '' as porcentaje,
    2 as orden
FROM table_counts
UNION ALL
SELECT 
    'Artistas coincidencias' as descripcion,
    matching_artists_count as cantidad,
    ROUND((matching_artists_count::decimal / spotify_artists_count * 100), 1) || '%' as porcentaje,
    3 as orden
FROM table_counts
UNION ALL
SELECT 
    'Canciones legacy' as descripcion,
    songs_count as cantidad,
    '' as porcentaje,
    4 as orden
FROM table_counts
UNION ALL
SELECT 
    'Canciones spotify' as descripcion,
    spotify_tracks_count as cantidad,
    '' as porcentaje,
    5 as orden
FROM table_counts
UNION ALL
SELECT 
    'Canciones coincidencias' as descripcion,
    matching_tracks_count as cantidad,
    ROUND((matching_tracks_count::decimal / spotify_tracks_count * 100), 1) || '%' as porcentaje,
    6 as orden
FROM table_counts
UNION ALL
SELECT 
    'Artista-Canción Legacy' as descripcion,
    song_artists_count as cantidad,
    '' as porcentaje,
    7 as orden
FROM table_counts
UNION ALL
SELECT 
    'Artista-Canción Spotify' as descripcion,
    spotify_track_artists_count as cantidad,
    '' as porcentaje,
    8 as orden
FROM table_counts
UNION ALL
SELECT 
    'Pares Artista-Canción MIGRADOS ✓' as descripcion,
    matching_unique_pairs_count as cantidad,
    ROUND((matching_unique_pairs_count::decimal / spotify_track_artists_count * 100), 1) || '%' as porcentaje,
    9 as orden
FROM table_counts
UNION ALL
SELECT 
    'Pares Artista-Canción FALTANTES ✗' as descripcion,
    missing_pairs_count as cantidad,
    ROUND((missing_pairs_count::decimal / spotify_track_artists_count * 100), 1) || '%' as porcentaje,
    10 as orden
FROM table_counts
UNION ALL
SELECT
    'spotify_albums' as descripcion,
    spotify_albums_count as cantidad,
    '' as porcentaje,
    11 as orden
FROM table_counts
UNION ALL
SELECT 
    'spotify_album_artists' as descripcion,
    spotify_album_artists_count as cantidad,
    '' as porcentaje,
    12 as orden
FROM table_counts
ORDER BY orden;