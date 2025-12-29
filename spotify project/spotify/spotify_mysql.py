import re
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

# Set up Spotify API credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='9ed300899c874eb7a3a70ed88a83fb9d',  # Replace with your Client ID
    client_secret='b2ae4c1c7ba24f719c332de9f2a6f017'  # Replace with your Client Secret
))

# MySQL Database Connection
db_config = {
    'host': 'localhost',           # Change to your MySQL host
    'user': 'root',       # Replace with your MySQL username
    'password': 'varun5526',   # Replace with your MySQL password
    'database': 'spotify'       # Replace with your database name
}

# Connect to the database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Full track URL (example: Shape of You by Ed Sheeran)
track_url = "https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp"

# Extract track ID directly from URL
track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)

# Fetch track details
track = sp.track(track_id)

# Extract metadata
track_data = {
    'Track Name': track['name'],
    'Artist': track['artists'][0]['name'],
    'Album': track['album']['name'],
    'Popularity': track['popularity'],
    'Duration (minutes)': track['duration_ms'] / 60000
}

# Insert data into MySQL
insert_query = """
INSERT INTO spotify_tracks (track_name, artist, album, popularity, duration_minutes)
VALUES (%s, %s, %s, %s, %s)
"""
cursor.execute(insert_query, (
    track_data['Track Name'],
    track_data['Artist'],
    track_data['Album'],
    track_data['Popularity'],
    track_data['Duration (minutes)']
))
connection.commit()

print(f"Track '{track_data['Track Name']}' by {track_data['Artist']} inserted into the database.")

# Close the connection
cursor.close()
connection.close()
