# File: wikis.py
# Author: Luke Wagner
# Description:
# For each artist in artists.txt, get a link to their discography on Wikipedia
# Write output to artists.csv
# -------------------------------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup

print("\nFinding wiki links for all artists...")

# Read artists from artists.txt into artists array
with open('artists.txt', 'r') as f:
    artists = [line.strip() for line in f]

with open('data/artists.csv', 'w') as f:
    f.write('Artist,Link\n') # write artist.csv header

    # Search for each artist's discography on Wikipedia and write it to artists.csv
    for artist in artists:
        # Construct the Wikipedia search URL
        # Search for "artist name discography"
        url = f'https://en.wikipedia.org/w/index.php?search={artist} discography'
        
        # Send a GET request to the URL
        response = requests.get(url)
        
        # If a result was found, write it to the output file
        link = response.url
        
        if 'https://en.wikipedia.org/w/index.php?search=' in link:
            # In this case, no page was found specifically for this artist's discography. 
            # Search again but this time just for "artist name," and append "#Discography" to the end
            url = f'https://en.wikipedia.org/w/index.php?search={artist}#Discography'
            response = requests.get(url)
            link = response.url

            # Write to the output file
            f.write(f'{artist},{link}\n')
        else:
            # In this case, a page was found specifically for this artist's discography.
            # Write to the output file
            f.write(f'{artist},{link}\n')