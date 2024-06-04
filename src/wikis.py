import requests
from bs4 import BeautifulSoup

# Read the list of artists from top_100.txt
with open('top_100.txt', 'r') as f:
    artists = [line.strip() for line in f]

# Search for each artist's discography on Wikipedia
with open('data/artists.csv', 'w') as f:
    f.write('Artist,Link\n')

    for artist in artists:
        # Construct the Wikipedia search URL
        url = f'https://en.wikipedia.org/w/index.php?search={artist} discography'
        
        # Send a GET request to the URL
        response = requests.get(url)
        
        # If a result was found, write it to the output file
        link = response.url
        if 'https://en.wikipedia.org/w/index.php?search=' in link:
            url = f'https://en.wikipedia.org/w/index.php?search={artist}#Discography'
            response = requests.get(url)
            link = response.url
            f.write(f'{artist},{link}\n')
        else:
            f.write(f'{artist},{link}\n')