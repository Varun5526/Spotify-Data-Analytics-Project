# Spotify-Data-Analytics-Project
👨‍💻 What I Did in This Project

In this project, I built a complete end-to-end data analytics pipeline. Here is a summary of my work:

1.  **Connected to Spotify API**: I configured the Spotify API with my credentials (`client_id` and `client_secret`) to authenticate and fetch real-time music data.
2.  **Built a MySQL Database**: I designed a relational database schema (`spotify_tracks` table) to store music metadata like track name, artist, album, popularity, and duration.
3.  **Developed Python ETL Scripts**: 
    *   I wrote scripts to fetch data for single tracks.
    *   I created a batch processor to read a list of URLs from a text file and automatically populate the database.
4.  **Performed Data Cleaning**: I wrote SQL queries to identify and remove duplicate track entries to ensure data integrity.
5.  **Conducted SQL Analysis**: I ran complex SQL queries to find top tracks, analyze artist performance, and study popularity trends.
6.  **Created a Visual Dashboard**: I built a Python script that generates:
    *   **Visualizations**: Bar charts, pie charts, and scatter plots using Matplotlib/Seaborn.
    *   **Interactive HTML Interface**: A professional, Spotify-themed web dashboard to display the insights.

---

## � Project Workflow Diagram

The following diagram illustrates the exact architecture and workflow I implemented:

![Spotify Project Flowchart](project_flowchart.png)

---

## 📂 Detailed Step-By-Step Breakdown

### Step 1: Database Setup 🛠️
I started by setting up the storage foundation.
- **File**: `spotify.sql`
- **Action**: Created the `spotify` database and `spotify_tracks` table.
- **Key Columns**: `track_name`, `artist`, `album`, `popularity`, `duration_minutes`.

### Step 2: Data Ingestion 📥
I needed a way to get data from Spotify into my local database.
- **File**: `spotify_mysql_urls.py`
- **Action**: This script reads links from `track_urls.txt`, calls the Spotify API, and saves the details to MySQL.

### Step 3: Data Cleaning 🧹
To ensure my analysis was accurate, I removed duplicate records.
- **File**: `remove_duplicates.sql`
- **Action**: Used SQL `DELETE` with a self-join to keep only unique track entries.

### Step 4: Data Visualization 📊
I wanted to see the stories hidden in the data.
- **File**: `generate_dashboard.py`
- **Action**: This script connects to the database, runs aggregation queries (e.g., "Top 5 Popular Tracks"), and uses Python's Matplotlib library to draw charts.

### Step 5: Dashboard Creation 🖥️
Finally, I brought it all together.
- **File**: `spotify_dashboard.html`
- **Action**: Generated a responsive HTML file that embeds the charts and displays key metrics (Total Tracks, Unique Artists) in a clean, dark-themed layout matching Spotify's brand.

## 🚀 How to Run My Project

1.  **Install Requirements**:
    ```bash
    pip install mysql-connector-python pandas matplotlib seaborn spotipy
    ```
2.  **Run the Generator**:
    ```bash
    python spotify/generate_dashboard.py
    ```
3.  **View the Dashboard**:
    Open `spotify_dashboard.html` in your browser.

---
*Created by Varun - Data Analytics Project 2025*

