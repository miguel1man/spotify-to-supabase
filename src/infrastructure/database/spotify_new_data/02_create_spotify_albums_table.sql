CREATE TABLE public.spotify_albums (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    spotify_id VARCHAR(100) NOT NULL UNIQUE,
    name TEXT NOT NULL,
    release_date TEXT,
    spotify_url VARCHAR(255),
    album_type TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_spotify_albums_spotify_id ON public.spotify_albums(spotify_id);
CREATE INDEX idx_spotify_albums_album_type ON public.spotify_albums(album_type);

ALTER TABLE public.spotify_albums ENABLE ROW LEVEL SECURITY;

CREATE POLICY "service_role_can_manage_spotify_albums" ON public.spotify_albums
FOR ALL TO service_role USING (true) WITH CHECK (true);
