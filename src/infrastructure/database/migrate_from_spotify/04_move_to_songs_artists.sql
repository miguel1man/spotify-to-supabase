-- Script para poblar los campos nulos en la tabla song_artists
-- Actualiza song_title cuando es NULL
UPDATE song_artists 
SET song_title = songs.title
FROM songs
WHERE song_artists.song_id = songs.id 
  AND song_artists.song_title IS NULL;

-- Actualiza artist_name cuando es NULL
UPDATE song_artists 
SET artist_name = artists.name
FROM artists
WHERE song_artists.artist_id = artists.id 
  AND song_artists.artist_name IS NULL;
