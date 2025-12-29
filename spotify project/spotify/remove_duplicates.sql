-- Remove Duplicates from spotify_tracks table
USE spotify;

-- Step 1: Check for duplicates before removing
SELECT track_name, artist, COUNT(*) as duplicate_count
FROM spotify_tracks
GROUP BY track_name, artist
HAVING COUNT(*) > 1;

-- Step 2: Remove duplicates (keep the first occurrence with lowest id)
DELETE t1 FROM spotify_tracks t1
INNER JOIN spotify_tracks t2 
WHERE t1.id > t2.id 
AND t1.track_name = t2.track_name 
AND t1.artist = t2.artist;

-- Step 3: Verify duplicates are removed
SELECT track_name, artist, COUNT(*) as duplicate_count
FROM spotify_tracks
GROUP BY track_name, artist
HAVING COUNT(*) > 1;

-- Step 4: View all remaining tracks
SELECT * FROM spotify_tracks ORDER BY id;
