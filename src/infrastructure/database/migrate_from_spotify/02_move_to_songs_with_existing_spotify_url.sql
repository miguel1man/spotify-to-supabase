-- Actualizar con contador de filas afectadas
WITH updated_rows AS (
    UPDATE songs 
    SET 
        spotify_track_id = st.spotify_track_id,
        spotify_url = st.spotify_url,
        spotify_saved_date = st.added_at,
        album_id = st.album_id,
        updated_at = NOW()
    FROM spotify_tracks st
    WHERE LOWER(TRIM(songs.title)) = LOWER(TRIM(st.track_name))
    AND NOT EXISTS (
        SELECT 1 FROM songs s2 
        WHERE s2.spotify_url = st.spotify_url 
        AND s2.id != songs.id
    )
    RETURNING songs.id, songs.title
)
SELECT 'FILAS ACTUALIZADAS: ' || COUNT(*) || ' registros' as resultado
FROM updated_rows;


-- Insertar nuevos registros que no existen en songs
INSERT INTO songs (title, spotify_track_id, spotify_url, spotify_saved_date, album_id, artist, created_at, updated_at)
SELECT 
    st.track_name,
    st.spotify_track_id,
    st.spotify_url,
    st.added_at,
    st.album_id,
    '-',
    st.created_at,
    NOW()
FROM spotify_tracks st
WHERE NOT EXISTS (
    SELECT 1 
    FROM songs s 
    WHERE LOWER(TRIM(s.title)) = LOWER(TRIM(st.track_name))
)
AND NOT EXISTS (
    SELECT 1 
    FROM songs s2 
    WHERE s2.spotify_url = st.spotify_url
);