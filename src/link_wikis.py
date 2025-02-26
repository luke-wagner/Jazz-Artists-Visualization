# File: link_wikis.py
# Author: Luke Wagner
# Description:
# For each artist in artists.txt, get a link to their discography on Wikipedia
# Store information found in artists table
# -------------------------------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup
import sqlite3

print("\nFinding wiki links for all artists...\n")

# Read artists from artists.txt into artists array
with open('artists.txt', 'r') as f:
    artists = [line.strip() for line in f]

# Remove artists already in artist_wikis table
conn = sqlite3.connect('data/main.db')
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT artist_name FROM artists WHERE link IS NOT NULL")
existing_artists = cursor.fetchall()
conn.close()

for artist in existing_artists:
    artists.remove(artist[0])

print("Number new artists to search for: " + str(len(artists)) + '\n')

# Search for each artist's discography on Wikipedia and add to artists table
for artist in artists:
    print("Searching for artist: " + artist)

    # Construct the Wikipedia search URL
    # Search for "artist name discography"
    url = f'https://en.wikipedia.org/w/index.php?search={artist} discography'
    
    # Send a GET request to the URL
    response = requests.get(url)
    
    # If a result was found, write it to the output file
    link = response.url
    
    if 'https://en.wikipedia.org/w/index.php?search=' in link:
        # In this case, no page was found specifically for this artist's discography. 
        discography_found = False

        # Search again but this time just for "artist name," and append "#Discography" to the end
        url = f'https://en.wikipedia.org/w/index.php?search={artist}#Discography'
        response = requests.get(url)
        link = response.url
    else:
        # In this case, a page was found specifically for this artist's discography.
        discography_found = True

    # Insert row into artists table, update on existing entry found
    conn = sqlite3.connect('data/main.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO artists (artist_name, link, discography_found)
        VALUES (?, ?, ?)
        ON CONFLICT(artist_name) DO UPDATE SET
            artist_name = excluded.artist_name,
            link = excluded.link,
            discography_found = excluded.discography_found;
    """, (artist, link, discography_found))
    conn.commit()
    conn.close()