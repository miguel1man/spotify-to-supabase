-- Create song_artists table
CREATE TABLE song_artists (
    song_id UUID NOT NULL,
    artist_id UUID NOT NULL,
    song_title TEXT,
    artist_name TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (song_id, artist_id),
    FOREIGN KEY (artist_id) REFERENCES artists(id),
    FOREIGN KEY (song_id) REFERENCES songs(id)
);