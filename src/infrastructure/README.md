# Infrastructure Layer

This directory contains the infrastructure components for the Spotify to Supabase project, including database migrations, configuration, and security settings.

## Database Schema

The database schema consists of the following tables and views for storing Spotify data synchronized with Supabase.

### Tables

#### 1. `spotify_artists`

Stores information about Spotify artists.

- `id` (UUID, Primary Key): Unique identifier
- `spotify_id` (VARCHAR(100), Unique, Not Null): Spotify's artist ID
- `name` (TEXT, Not Null): Artist name
- `spotify_url` (VARCHAR(255)): Spotify URL for the artist
- `created_at` (TIMESTAMP WITH TIME ZONE): Record creation timestamp
- `updated_at` (TIMESTAMP WITH TIME ZONE): Record update timestamp

**Indexes:**

- `idx_spotify_artists_spotify_id` on `spotify_id`

**Row Level Security:** Enabled with service_role policy for full access.

#### 2. `spotify_albums`

Stores information about Spotify albums.

- `id` (UUID, Primary Key): Unique identifier
- `spotify_id` (VARCHAR(100), Unique, Not Null): Spotify's album ID
- `name` (TEXT, Not Null): Album name
- `release_date` (TEXT): Album release date
- `spotify_url` (VARCHAR(255)): Spotify URL for the album
- `album_type` (TEXT): Type of album (e.g., "album", "single", "compilation")
- `created_at` (TIMESTAMP WITH TIME ZONE): Record creation timestamp
- `updated_at` (TIMESTAMP WITH TIME ZONE): Record update timestamp

**Indexes:**

- `idx_spotify_albums_spotify_id` on `spotify_id`
- `idx_spotify_albums_album_type` on `album_type`

**Row Level Security:** Enabled with service_role policy for full access.

#### 3. `spotify_tracks`

Stores information about Spotify tracks.

- `id` (UUID, Primary Key): Unique identifier
- `spotify_track_id` (VARCHAR(100), Unique, Not Null): Spotify's track ID
- `track_name` (TEXT, Not Null): Track name
- `spotify_url` (VARCHAR(255)): Spotify URL for the track
- `added_at` (TIMESTAMP WITH TIME ZONE, Not Null): When the track was added
- `album_id` (UUID, Foreign Key to `spotify_albums.id`): Reference to the album
- `created_at` (TIMESTAMP WITH TIME ZONE): Record creation timestamp
- `updated_at` (TIMESTAMP WITH TIME ZONE): Record update timestamp

**Indexes:**

- `idx_spotify_tracks_spotify_id` on `spotify_track_id`
- `idx_spotify_tracks_album_id` on `album_id`

**Row Level Security:** Enabled with service_role policy for full access.

#### 4. `spotify_track_artists` (Junction Table)

Manages many-to-many relationship between tracks and artists.

- `track_id` (UUID, Not Null, Foreign Key to `spotify_tracks.id`): Track reference
- `artist_id` (UUID, Not Null, Foreign Key to `spotify_artists.id`): Artist reference
- `artist_name` (TEXT, Not Null): Artist name (denormalized)
- `spotify_track_name` (TEXT, Not Null): Track name (denormalized)
- `created_at` (TIMESTAMP WITH TIME ZONE): Record creation timestamp

**Primary Key:** Composite on (`track_id`, `artist_id`)

**Indexes:**

- `idx_spotify_track_artists_track_id` on `track_id`
- `idx_spotify_track_artists_artist_id` on `artist_id`

**Row Level Security:** Enabled with service_role policy for full access.

#### 5. `spotify_album_artists` (Junction Table)

Manages many-to-many relationship between albums and artists.

- `album_id` (UUID, Not Null, Foreign Key to `spotify_albums.id`): Album reference
- `artist_id` (UUID, Not Null, Foreign Key to `spotify_artists.id`): Artist reference
- `artist_name` (TEXT, Not Null): Artist name (denormalized)
- `album_name` (TEXT, Not Null): Album name (denormalized)
- `created_at` (TIMESTAMP WITH TIME ZONE): Record creation timestamp

**Primary Key:** Composite on (`album_id`, `artist_id`)

**Indexes:**

- `idx_spotify_album_artists_album_id` on `album_id`
- `idx_spotify_album_artists_artist_id` on `artist_id`

**Row Level Security:** Enabled with service_role policy for full access.

### Views

#### `track_details`

A view that provides a readable summary of tracks with their associated albums and artists.

**Columns:**

- `track_id` (UUID): Track ID
- `track_name` (TEXT): Track name
- `spotify_url` (VARCHAR(255)): Spotify URL
- `album_name` (TEXT): Album name
- `artists_names` (TEXT): Comma-separated list of artist names

**Permissions:** SELECT granted to service_role.

## Migration Files

The database schema is defined through the following migration files in `database/migrations/`:

1. `01_create_spotify_artists_table.sql` - Creates the artists table
2. `02_create_spotify_albums_table.sql` - Creates the albums table
3. `03_create_spotify_tracks_table.sql` - Creates the tracks table
4. `04_create_spotify_track_artists_table.sql` - Creates the track-artists junction table
5. `05_create_spotify_album_artists_table.sql` - Creates the album-artists junction table
6. `06_create_track_details_view.sql` - Creates the track details view

## Notes

- All tables use UUID primary keys with automatic generation.
- Foreign key constraints are set with appropriate cascade/delete behaviors.
- Row Level Security (RLS) is enabled on all tables with policies allowing service_role full access.
- Indexes are created on frequently queried columns for performance.
- The `album_type` column in `spotify_albums` uses TEXT for flexibility, accommodating potential future album types beyond "album" and "single".
