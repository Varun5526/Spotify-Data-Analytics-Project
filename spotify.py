from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import re

matplotlib.use('Agg')  # Use non-interactive backend

# Set up Client Credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='9ed300899c874eb7a3a70ed88a83fb9d',  # Replace with your Client ID
    client_secret='b2ae4c1c7ba24f719c332de9f2a6f017'  # Replace with your Client Secret
))

# Full track URL (example: Shape of You by Ed Sheeran)
track_url = "https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp"

# Extract track ID directly from URL using regex
track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)

# Fetch track details
track = sp.track(track_id)        #it will fetch the track details using the track id 
print(track)                      #stores as json format


# Extract metadata
track_data = {
    'Track Name': track['name'],
    'Artist': track['artists'][0]['name'],
    'Album': track['album']['name'],
    'Popularity': track['popularity'],
    'Duration (minutes)': track['duration_ms'] / 60000
}

# Display metadata
print(f"\nTrack Name: {track_data['Track Name']}")
print(f"Artist: {track_data['Artist']}")
print(f"Album: {track_data['Album']}")
print(f"Popularity: {track_data['Popularity']}")
print(f"Duration: {track_data['Duration (minutes)']:.2f} minutes")

# Convert metadata to DataFrame
df = pd.DataFrame([track_data])
print("\nTrack Data as DataFrame:")
print(df)

# Save metadata to CSV
df.to_csv('spotify_track_data.csv', index=False)

# Visualize track data
features = ['Popularity', 'Duration (minutes)']
values = [track_data['Popularity'], track_data['Duration (minutes)']]

plt.figure(figsize=(8, 5))
plt.bar(features, values, color='skyblue', edgecolor='black')
plt.title(f"Track Metadata for '{track_data['Track Name']}'")
plt.ylabel('Value')
plt.savefig('track_visualization.png')
print("Plot saved as track_visualization.png")
# plt.show()