-- Create songs table
CREATE TABLE songs (
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    previous_score NUMERIC,
    score_2024_10 NUMERIC,
    score_2024_q3 NUMERIC,
    score_2024_q2 NUMERIC,
    score_2024_q1 NUMERIC,
    score_2023 NUMERIC,
    album_date DATE,
    language TEXT,
    genre TEXT,
    playlists_name TEXT,
    energy NUMERIC,
    youtube_url TEXT,
    youtube_views BIGINT,
    spotify_url TEXT,
    album_name TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    current_score NUMERIC,
    score_2024_11 NUMERIC,
    score_2025_02 NUMERIC,
    score_2025_01 NUMERIC,
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    Ciudad TEXT,
    País TEXT,
    spotify_track_id VARCHAR(100),
    album_id UUID REFERENCES public.spotify_albums(id) ON DELETE SET NULL,
    spotify_saved_date TIMESTAMP WITH TIME ZONE
);

-- Add unique constraints
ALTER TABLE songs ADD CONSTRAINT songs_youtube_url_key UNIQUE (youtube_url);
ALTER TABLE songs ADD CONSTRAINT songs_spotify_url_key UNIQUE (spotify_url);
ALTER TABLE songs ADD CONSTRAINT songs_id_key UNIQUE (id);
ALTER TABLE songs ADD CONSTRAINT songs_spotify_track_id_key UNIQUE (spotify_track_id);