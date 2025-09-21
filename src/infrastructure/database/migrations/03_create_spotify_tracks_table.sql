CREATE TABLE public.spotify_tracks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    spotify_track_id VARCHAR(100) NOT NULL UNIQUE,
    track_name TEXT NOT NULL,
    spotify_url VARCHAR(255),
    added_at TIMESTAMP WITH TIME ZONE NOT NULL,
    album_id UUID REFERENCES public.spotify_albums(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_spotify_tracks_spotify_id ON public.spotify_tracks(spotify_track_id);
CREATE INDEX idx_spotify_tracks_album_id ON public.spotify_tracks(album_id);

ALTER TABLE public.spotify_tracks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "service_role_can_manage_spotify_tracks" ON public.spotify_tracks
FOR ALL TO service_role USING (true) WITH CHECK (true);
