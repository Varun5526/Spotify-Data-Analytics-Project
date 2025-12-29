-- Spotify Data Analysis Queries
USE spotify;

-- 1. Most Popular Track
SELECT track_name, artist, album, popularity
FROM spotify_tracks
ORDER BY popularity DESC
LIMIT 1;

-- 2. Top 5 Most Popular Tracks
SELECT track_name, artist, popularity
FROM spotify_tracks
ORDER BY popularity DESC
LIMIT 5;

-- 3. Average Popularity
SELECT AVG(popularity) AS average_popularity
FROM spotify_tracks;

-- 4. Tracks Longer Than 4 Minutes
SELECT track_name, artist, duration_minutes
FROM spotify_tracks
WHERE duration_minutes > 4.0
ORDER BY duration_minutes DESC;

-- 5. Popularity Distribution
SELECT 
    CASE 
        WHEN popularity >= 80 THEN 'Very Popular'
        WHEN popularity >= 50 THEN 'Popular'
        ELSE 'Less Popular'
    END AS popularity_range,
    COUNT(*) AS track_count
FROM spotify_tracks
GROUP BY popularity_range
ORDER BY track_count DESC;

-- 6. Average Duration by Popularity Range
SELECT 
    CASE 
        WHEN popularity >= 80 THEN 'Very Popular'
        WHEN popularity >= 50 THEN 'Popular'
        ELSE 'Less Popular'
    END AS popularity_range,
    AVG(duration_minutes) AS avg_duration,
    COUNT(*) AS track_count
FROM spotify_tracks
GROUP BY popularity_range;

-- 7. Top Artists by Track Count
SELECT artist, COUNT(*) AS track_count, AVG(popularity) AS avg_popularity
FROM spotify_tracks
GROUP BY artist
ORDER BY track_count DESC, avg_popularity DESC;

-- 8. Summary Statistics
SELECT 
    COUNT(*) AS total_tracks,
    COUNT(DISTINCT artist) AS unique_artists,
    COUNT(DISTINCT album) AS unique_albums,
    AVG(popularity) AS avg_popularity,
    MAX(popularity) AS max_popularity,
    MIN(popularity) AS min_popularity,
    AVG(duration_minutes) AS avg_duration
FROM spotify_tracks;

-- 9. All Tracks
SELECT * FROM spotify_tracks ORDER BY popularity DESC;