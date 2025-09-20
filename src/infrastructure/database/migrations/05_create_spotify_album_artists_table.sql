-- 5. Tabla de Unión: Album-Artists
-- Maneja la relación muchos a muchos entre álbumes y artistas.
CREATE TABLE public.spotify_album_artists (
    album_id UUID NOT NULL REFERENCES public.spotify_albums(id) ON DELETE CASCADE,
    artist_id UUID NOT NULL REFERENCES public.spotify_artists(id) ON DELETE CASCADE,
    PRIMARY KEY (album_id, artist_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_spotify_album_artists_album_id ON public.spotify_album_artists(album_id);
CREATE INDEX idx_spotify_album_artists_artist_id ON public.spotify_album_artists(artist_id);

ALTER TABLE public.spotify_album_artists ENABLE ROW LEVEL SECURITY;

CREATE POLICY "service_role_can_manage_album_artists" ON public.spotify_album_artists
FOR ALL TO service_role USING (true) WITH CHECK (true);
