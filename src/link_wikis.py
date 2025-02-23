# File: link_wikis.py
# Author: Luke Wagner
# Description:
# For each artist in artists.txt, get a link to their discography on Wikipedia
# Write output to artists.csv
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
cursor.execute("SELECT DISTINCT artist_name FROM artist_wikis")
existing_artists = cursor.fetchall()
conn.close()

for artist in existing_artists:
    artists.remove(artist[0])

print("Number new artists to search for: " + str(len(artists)) + '\n')

with open('data/artists.csv', 'w') as f:
    f.write('Artist,Link\n') # write artist.csv header

    # Search for each artist's discography on Wikipedia and write it to artists.csv
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
            
            # Write to the output file
            f.write(f'{artist},{link}\n')
        else:
            # In this case, a page was found specifically for this artist's discography.
            discography_found = True

            # Write to the output file
            f.write(f'{artist},{link}\n')

        # Insert row into artist_wikis table
        conn = sqlite3.connect('data/main.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO artist_wikis (artist_name, link, discography_found) VALUES (?, ?, ?)", (artist, link, discography_found))
        conn.commit()
        conn.close()