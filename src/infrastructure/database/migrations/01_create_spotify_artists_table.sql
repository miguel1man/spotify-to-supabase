CREATE TABLE public.spotify_artists (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    spotify_id VARCHAR(100) NOT NULL UNIQUE,
    name TEXT NOT NULL,
    spotify_url VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_spotify_artists_spotify_id ON public.spotify_artists(spotify_id);

ALTER TABLE public.spotify_artists ENABLE ROW LEVEL SECURITY;

CREATE POLICY "service_role_can_manage_spotify_artists" ON public.spotify_artists
FOR ALL TO service_role USING (true) WITH CHECK (true);
