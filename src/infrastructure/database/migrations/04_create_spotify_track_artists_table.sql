-- Tabla de Unión: Track-Artists
CREATE TABLE public.spotify_track_artists (
    track_id UUID NOT NULL REFERENCES public.spotify_tracks(id) ON DELETE CASCADE,
    artist_id UUID NOT NULL REFERENCES public.spotify_artists(id) ON DELETE CASCADE,
    artist_name TEXT NOT NULL,
    spotify_track_name TEXT NOT NULL,
    PRIMARY KEY (track_id, artist_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_spotify_track_artists_track_id ON public.spotify_track_artists(track_id);
CREATE INDEX idx_spotify_track_artists_artist_id ON public.spotify_track_artists(artist_id);

ALTER TABLE public.spotify_track_artists ENABLE ROW LEVEL SECURITY;

CREATE POLICY "service_role_can_manage_track_artists" ON public.spotify_track_artists
FOR ALL TO service_role USING (true) WITH CHECK (true);
