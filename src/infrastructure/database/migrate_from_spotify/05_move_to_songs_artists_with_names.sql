-- Query para migrar los elementos faltantes de spotify_track_artists a song_artists
-- Basado en coincidencias de nombres (no en IDs de Spotify)

DO $$
DECLARE
    inserted_count INTEGER;
    missing_count INTEGER;
BEGIN
    -- 1. Primero verificar cuántos elementos faltan
    SELECT COUNT(*) INTO missing_count
    FROM spotify_track_artists sta
    WHERE NOT EXISTS (
        SELECT 1 FROM song_artists sa 
        WHERE LOWER(TRIM(sa.song_title)) = LOWER(TRIM(sta.spotify_track_name))
        AND LOWER(TRIM(sa.artist_name)) = LOWER(TRIM(sta.artist_name))
    );
    
    RAISE NOTICE 'Elementos faltantes detectados: %', missing_count;
    
    -- 2. Insertar los elementos faltantes
    INSERT INTO song_artists (song_id, artist_id, song_title, artist_name)
    SELECT DISTINCT
        s.id as song_id,
        a.id as artist_id,
        sta.spotify_track_name as song_title,
        sta.artist_name as artist_name
    FROM spotify_track_artists sta
    INNER JOIN songs s ON LOWER(TRIM(s.title)) = LOWER(TRIM(sta.spotify_track_name))
    INNER JOIN artists a ON LOWER(TRIM(a.name)) = LOWER(TRIM(sta.artist_name))
    WHERE NOT EXISTS (
        SELECT 1 FROM song_artists sa 
        WHERE sa.song_id = s.id 
        AND sa.artist_id = a.id
        AND LOWER(TRIM(sa.song_title)) = LOWER(TRIM(sta.spotify_track_name))
        AND LOWER(TRIM(sa.artist_name)) = LOWER(TRIM(sta.artist_name))
    );
    
    GET DIAGNOSTICS inserted_count = ROW_COUNT;
    
    RAISE NOTICE '==========================================';
    RAISE NOTICE 'MIGRACIÓN DE ELEMENTOS FALTANTES COMPLETADA';
    RAISE NOTICE '==========================================';
    RAISE NOTICE 'Registros insertados: %', inserted_count;
    RAISE NOTICE '==========================================';
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'ERROR en migración: %', SQLERRM;
        RAISE;
END $$;

-- Query de verificación después de la migración
WITH verification_stats AS (
    SELECT 
        (SELECT COUNT(*) FROM spotify_track_artists) as spotify_track_artists_total,
        (SELECT COUNT(*) FROM song_artists) as song_artists_total,
        (SELECT COUNT(*) 
         FROM spotify_track_artists sta 
         INNER JOIN song_artists sa ON LOWER(TRIM(sta.spotify_track_name)) = LOWER(TRIM(sa.song_title))
                                   AND LOWER(TRIM(sta.artist_name)) = LOWER(TRIM(sa.artist_name))
        ) as matching_after_migration,
        (SELECT COUNT(*) 
         FROM spotify_track_artists sta
         WHERE NOT EXISTS (
             SELECT 1 FROM song_artists sa 
             WHERE LOWER(TRIM(sa.song_title)) = LOWER(TRIM(sta.spotify_track_name))
             AND LOWER(TRIM(sa.artist_name)) = LOWER(TRIM(sta.artist_name))
         )
        ) as still_missing,
        NOW() as executed_at
)
SELECT 
    '🔍 VERIFICACIÓN POST-MIGRACIÓN' as titulo,
    spotify_track_artists_total as "📊 Total spotify_track_artists",
    song_artists_total as "📈 Total song_artists",
    matching_after_migration as "✅ Coincidencias encontradas",
    still_missing as "❌ Elementos aún faltantes",
    CASE 
        WHEN still_missing = 0 THEN '🎉 MIGRACIÓN COMPLETA'
        ELSE '⚠️ AÚN FALTAN ELEMENTOS'
    END as status,
    executed_at as "⏰ Ejecutado"
FROM verification_stats;