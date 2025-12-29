USE spotify;
CREATE TABLE IF NOT EXISTS spotify_tracks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    track_name VARCHAR(255),
    artist VARCHAR(255),
    album VARCHAR(255),
    popularity INT,
    duration_minutes FLOAT
);

TRUNCATE TABLE spotify_tracks;

INSERT INTO spotify_tracks (track_name, artist, album, popularity, duration_minutes) VALUES
    ('Blinding Lights', 'The Weeknd', 'After Hours', 95, 3.20),
    ('Levitating', 'Dua Lipa', 'Future Nostalgia', 92, 3.23),
    ('drivers license', 'Olivia Rodrigo', 'SOUR', 90, 4.02),
    ('Bad Habit', 'Steve Lacy', 'Gemini Rights', 88, 3.52),
    ('As It Was', 'Harry Styles', 'Harry''s House', 94, 2.47);

SELECT * FROM spotify_tracks;