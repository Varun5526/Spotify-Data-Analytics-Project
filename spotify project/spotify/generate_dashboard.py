import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = '#0A0E27'
plt.rcParams['axes.facecolor'] = '#1a1f3a'
plt.rcParams['text.color'] = '#FFFFFF'
plt.rcParams['axes.labelcolor'] = '#FFFFFF'
plt.rcParams['xtick.color'] = '#FFFFFF'
plt.rcParams['ytick.color'] = '#FFFFFF'

# MySQL Database Connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'varun5526',
    'database': 'spotify'
}

try:
    # Connect to the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    
    # Query 1: Get all tracks
    cursor.execute("SELECT * FROM spotify_tracks ORDER BY popularity DESC")
    all_tracks = cursor.fetchall()
    df_tracks = pd.DataFrame(all_tracks)
    
    # Query 2: Summary Statistics
    cursor.execute("""
        SELECT 
            COUNT(*) AS total_tracks,
            COUNT(DISTINCT artist) AS unique_artists,
            COUNT(DISTINCT album) AS unique_albums,
            AVG(popularity) AS avg_popularity,
            MAX(popularity) AS max_popularity,
            MIN(popularity) AS min_popularity,
            AVG(duration_minutes) AS avg_duration
        FROM spotify_tracks
    """)
    summary_stats = cursor.fetchone()
    
    # Query 3: Top 5 Tracks
    cursor.execute("""
        SELECT track_name, artist, popularity
        FROM spotify_tracks
        ORDER BY popularity DESC
        LIMIT 5
    """)
    top_tracks = cursor.fetchall()
    
    # Query 4: Popularity Distribution
    cursor.execute("""
        SELECT 
            CASE 
                WHEN popularity >= 80 THEN 'Very Popular'
                WHEN popularity >= 50 THEN 'Popular'
                ELSE 'Less Popular'
            END AS popularity_range,
            COUNT(*) AS track_count
        FROM spotify_tracks
        GROUP BY popularity_range
        ORDER BY track_count DESC
    """)
    popularity_dist = cursor.fetchall()
    
    # Query 5: Top Artists
    cursor.execute("""
        SELECT artist, COUNT(*) AS track_count, AVG(popularity) AS avg_popularity
        FROM spotify_tracks
        GROUP BY artist
        ORDER BY track_count DESC, avg_popularity DESC
        LIMIT 5
    """)
    top_artists = cursor.fetchall()
    
    # Close database connection
    cursor.close()
    connection.close()
    
    # Create visualizations
    fig = plt.figure(figsize=(20, 12))
    fig.suptitle('🎵 Spotify Analytics Dashboard', fontsize=28, fontweight='bold', color='#1DB954', y=0.98)
    
    # 1. Top 5 Tracks Bar Chart
    ax1 = plt.subplot(2, 3, 1)
    top_df = pd.DataFrame(top_tracks)
    bars = ax1.barh(top_df['track_name'], top_df['popularity'], color='#1DB954', edgecolor='#1ed760', linewidth=2)
    ax1.set_xlabel('Popularity Score', fontsize=12, fontweight='bold')
    ax1.set_title('🏆 Top 5 Most Popular Tracks', fontsize=14, fontweight='bold', color='#1DB954', pad=15)
    ax1.grid(axis='x', alpha=0.3)
    ax1.invert_yaxis()
    
    # 2. Popularity Distribution Pie Chart
    ax2 = plt.subplot(2, 3, 2)
    pop_df = pd.DataFrame(popularity_dist)
    colors = ['#1DB954', '#1ed760', '#535353']
    wedges, texts, autotexts = ax2.pie(pop_df['track_count'], labels=pop_df['popularity_range'], 
                                         autopct='%1.1f%%', startangle=90, colors=colors,
                                         textprops={'color': 'white', 'fontsize': 11, 'fontweight': 'bold'})
    ax2.set_title('📊 Popularity Distribution', fontsize=14, fontweight='bold', color='#1DB954', pad=15)
    
    # 3. Duration vs Popularity Scatter
    ax3 = plt.subplot(2, 3, 3)
    scatter = ax3.scatter(df_tracks['duration_minutes'], df_tracks['popularity'], 
                          c=df_tracks['popularity'], cmap='viridis', s=200, alpha=0.7, edgecolors='white', linewidth=2)
    ax3.set_xlabel('Duration (minutes)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Popularity Score', fontsize=12, fontweight='bold')
    ax3.set_title('⏱️ Duration vs Popularity', fontsize=14, fontweight='bold', color='#1DB954', pad=15)
    ax3.grid(alpha=0.3)
    plt.colorbar(scatter, ax=ax3, label='Popularity')
    
    # 4. Top Artists
    ax4 = plt.subplot(2, 3, 4)
    artists_df = pd.DataFrame(top_artists)
    bars = ax4.bar(range(len(artists_df)), artists_df['track_count'], color='#1ed760', edgecolor='#1DB954', linewidth=2)
    ax4.set_xticks(range(len(artists_df)))
    ax4.set_xticklabels(artists_df['artist'], rotation=45, ha='right')
    ax4.set_ylabel('Number of Tracks', fontsize=12, fontweight='bold')
    ax4.set_title('🎤 Top Artists by Track Count', fontsize=14, fontweight='bold', color='#1DB954', pad=15)
    ax4.grid(axis='y', alpha=0.3)
    
    # 5. Popularity Histogram
    ax5 = plt.subplot(2, 3, 5)
    ax5.hist(df_tracks['popularity'], bins=10, color='#1DB954', edgecolor='#1ed760', linewidth=2, alpha=0.8)
    ax5.set_xlabel('Popularity Score', fontsize=12, fontweight='bold')
    ax5.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax5.set_title('📈 Popularity Distribution Histogram', fontsize=14, fontweight='bold', color='#1DB954', pad=15)
    ax5.grid(axis='y', alpha=0.3)
    
    # 6. Summary Statistics Box
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('off')
    
    stats_text = f"""
    📊 SUMMARY STATISTICS
    
    Total Tracks: {summary_stats['total_tracks']}
    Unique Artists: {summary_stats['unique_artists']}
    Unique Albums: {summary_stats['unique_albums']}
    
    Average Popularity: {summary_stats['avg_popularity']:.1f}
    Max Popularity: {summary_stats['max_popularity']}
    Min Popularity: {summary_stats['min_popularity']}
    
    Avg Duration: {summary_stats['avg_duration']:.2f} min
    """
    
    ax6.text(0.1, 0.5, stats_text, fontsize=14, verticalalignment='center',
             bbox=dict(boxstyle='round', facecolor='#1a1f3a', edgecolor='#1DB954', linewidth=3, alpha=0.9),
             color='#FFFFFF', fontweight='bold', family='monospace')
    
    plt.tight_layout()
    plt.savefig('spotify_dashboard.png', dpi=300, bbox_inches='tight', facecolor='#0A0E27')
    print("✅ Dashboard visualizations saved as 'spotify_dashboard.png'")
    
    # Generate HTML Dashboard
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Spotify Analytics Dashboard</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
                color: #ffffff;
                padding: 20px;
                min-height: 100vh;
            }}
            
            .container {{
                max-width: 1400px;
                margin: 0 auto;
            }}
            
            header {{
                text-align: center;
                padding: 40px 20px;
                background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
                border-radius: 20px;
                box-shadow: 0 10px 40px rgba(29, 185, 84, 0.3);
                margin-bottom: 40px;
            }}
            
            .logo {{
                width: 70px;
                height: 70px;
                margin: 0 auto 15px;
            }}
            
            .logo svg {{
                width: 100%;
                height: 100%;
                filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
            }}
            
            h1 {{
                font-size: 3em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }}
            
            .subtitle {{
                font-size: 1.2em;
                opacity: 0.9;
            }}
            
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }}
            
            .stat-card {{
                background: linear-gradient(135deg, #1a1f3a 0%, #252b4a 100%);
                padding: 30px;
                border-radius: 15px;
                border: 2px solid #1DB954;
                box-shadow: 0 5px 20px rgba(0,0,0,0.3);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }}
            
            .stat-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 30px rgba(29, 185, 84, 0.4);
            }}
            
            .stat-icon {{
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            
            .stat-value {{
                font-size: 2.5em;
                font-weight: bold;
                color: #1DB954;
                margin: 10px 0;
            }}
            
            .stat-label {{
                font-size: 1.1em;
                opacity: 0.8;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            
            .section {{
                background: linear-gradient(135deg, #1a1f3a 0%, #252b4a 100%);
                padding: 30px;
                border-radius: 15px;
                margin-bottom: 30px;
                border: 2px solid #1DB954;
                box-shadow: 0 5px 20px rgba(0,0,0,0.3);
            }}
            
            .section h2 {{
                color: #1DB954;
                margin-bottom: 20px;
                font-size: 2em;
                border-bottom: 2px solid #1DB954;
                padding-bottom: 10px;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            
            th, td {{
                padding: 15px;
                text-align: left;
                border-bottom: 1px solid rgba(29, 185, 84, 0.2);
            }}
            
            th {{
                background: rgba(29, 185, 84, 0.2);
                color: #1DB954;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            
            tr:hover {{
                background: rgba(29, 185, 84, 0.1);
            }}
            
            .badge {{
                display: inline-block;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.9em;
                font-weight: bold;
                background: #1DB954;
                color: #0a0e27;
            }}
            
            .dashboard-image {{
                width: 100%;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.5);
                margin: 30px 0;
            }}
            
            .footer {{
                text-align: center;
                padding: 30px;
                margin-top: 40px;
                opacity: 0.6;
                font-size: 0.9em;
            }}
            
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.7; }}
            }}
            
            .pulse {{
                animation: pulse 2s infinite;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <div class="logo">
                    <svg viewBox="0 0 496 512" xmlns="http://www.w3.org/2000/svg">
                        <path fill="#FFFFFF" d="M248 8C111.1 8 0 119.1 0 256s111.1 248 248 248 248-111.1 248-248S384.9 8 248 8zm100.7 364.9c-4.2 0-6.8-1.3-10.7-3.6-62.4-37.6-135-39.2-206.7-24.5-3.9 1-9 2.6-11.9 2.6-9.7 0-15.8-7.7-15.8-15.8 0-10.3 6.1-15.2 13.6-16.8 81.9-18.1 165.6-16.5 237 26.2 6.1 3.9 9.7 7.4 9.7 16.5s-7.1 15.4-15.2 15.4zm26.9-65.6c-5.2 0-8.7-2.3-12.3-4.2-62.5-37-155.7-51.9-238.6-29.4-4.8 1.3-7.4 2.6-11.9 2.6-10.7 0-19.4-8.7-19.4-19.4s5.2-17.8 15.5-20.7c27.8-7.8 56.2-13.6 97.8-13.6 64.9 0 127.6 16.1 177 45.5 8.1 4.8 11.3 11 11.3 19.7-.1 10.8-8.5 19.5-19.4 19.5zm31-76.2c-5.2 0-8.4-1.3-12.9-3.9-71.2-42.5-198.5-52.7-280.9-29.7-3.6 1-8.1 2.6-12.9 2.6-13.2 0-23.3-10.3-23.3-23.6 0-13.6 8.4-21.3 17.4-23.9 35.2-10.3 74.6-15.2 117.5-15.2 73 0 149.5 15.2 205.4 47.8 7.8 4.5 12.9 10.7 12.9 22.6 0 13.6-11 23.3-23.2 23.3z"/>
                    </svg>
                </div>
                <h1>🎵 Spotify Analytics Dashboard</h1>
                <p class="subtitle">Data-Driven Music Insights | Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </header>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon">🎵</div>
                    <div class="stat-value">{summary_stats['total_tracks']}</div>
                    <div class="stat-label">Total Tracks</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">🎤</div>
                    <div class="stat-value">{summary_stats['unique_artists']}</div>
                    <div class="stat-label">Unique Artists</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">💿</div>
                    <div class="stat-value">{summary_stats['unique_albums']}</div>
                    <div class="stat-label">Unique Albums</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">⭐</div>
                    <div class="stat-value">{summary_stats['avg_popularity']:.1f}</div>
                    <div class="stat-label">Avg Popularity</div>
                </div>
            </div>
            
            <div class="section">
                <h2>📊 Visual Analytics</h2>
                <img src="spotify_dashboard.png" alt="Spotify Dashboard" class="dashboard-image">
            </div>
            
            <div class="section">
                <h2>🏆 Top 5 Most Popular Tracks</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Track Name</th>
                            <th>Artist</th>
                            <th>Popularity</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    for idx, track in enumerate(top_tracks, 1):
        html_content += f"""
                        <tr>
                            <td><span class="badge">#{idx}</span></td>
                            <td>{track['track_name']}</td>
                            <td>{track['artist']}</td>
                            <td><strong style="color: #1DB954;">{track['popularity']}</strong></td>
                        </tr>
        """
    
    html_content += """
                    </tbody>
                </table>
            </div>
            
            <div class="section">
                <h2>🎸 All Tracks in Database</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Track Name</th>
                            <th>Artist</th>
                            <th>Album</th>
                            <th>Popularity</th>
                            <th>Duration (min)</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    for track in all_tracks:
        html_content += f"""
                        <tr>
                            <td>{track['track_name']}</td>
                            <td>{track['artist']}</td>
                            <td>{track['album']}</td>
                            <td><strong style="color: #1DB954;">{track['popularity']}</strong></td>
                            <td>{track['duration_minutes']:.2f}</td>
                        </tr>
        """
    
    html_content += f"""
                    </tbody>
                </table>
            </div>
            
            <div class="footer">
                <p>🎵 Spotify Analytics Dashboard | Powered by MySQL & Python | © 2025</p>
                <p class="pulse">Data refreshed in real-time from your Spotify database</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Save HTML dashboard
    with open('spotify_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ HTML Dashboard saved as 'spotify_dashboard.html'")
    print("\n" + "="*60)
    print("📊 DASHBOARD GENERATION COMPLETE!")
    print("="*60)
    print(f"\n📁 Files Generated:")
    print(f"   1. spotify_dashboard.png  - Visual analytics")
    print(f"   2. spotify_dashboard.html - Interactive dashboard")
    print(f"\n🚀 Open 'spotify_dashboard.html' in your browser to view!")
    print("="*60)
    
except mysql.connector.Error as err:
    print(f"❌ Database Error: {err}")
except Exception as e:
    print(f"❌ Error: {e}")
