-- Create artists table with all columns
CREATE TABLE artists (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    name TEXT NOT NULL UNIQUE,
    spotify_id VARCHAR(100) UNIQUE,
    spotify_url VARCHAR(255)
);

-- Add additional unique constraint on id (though primary key implies unique)
ALTER TABLE artists ADD CONSTRAINT artists_id_key UNIQUE (id);

-- Create index on spotify_id for better performance
CREATE INDEX idx_artists_spotify_id ON artists(spotify_id);

-- Enable Row Level Security (optional, matching spotify_artists pattern)
ALTER TABLE artists ENABLE ROW LEVEL SECURITY;

-- Create policy for service role (optional, matching spotify_artists pattern)
CREATE POLICY "service_role_can_manage_artists" ON artists
FOR ALL TO service_role USING (true) WITH CHECK (true);