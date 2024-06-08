# File: clean_artists.py
# Author: Luke Wagner
# Description:
# Removes artists from artists.txt that do not have albums in albums.csv
# -------------------------------------------------------------------------------------------------

import pandas as pd
from colorama import Fore, Back, Style

# Get list of artists from artists.txt
with open('artists.txt', 'r') as f:
    artists_from_list = [line.strip() for line in f]

# Create set of all artists in albums.csv
df = pd.read_csv('data/albums.csv',on_bad_lines='skip', encoding='latin-1')
album_artists = set(df['Artist'].tolist())

no_albums = [] # list of artists with no albums

print("\nRemoving artists:\n")

# Print each artist not in album_artists
for artist in artists_from_list:
    if artist not in album_artists:
        print(artist)
        no_albums.append(artist)

# Print total artists with no albums
print("\nTotal artists with no albums: " + str(len(no_albums)))

# Replace content of artists.txt upon user confirmation
user_input = input("\nOverride artists.txt? (y/n) ")

if user_input.lower() != 'y':
    quit() # do not continue running script without user confirmation

# Replace content of artists.txt
with open('artists.txt', 'w') as f:
    for artist in artists_from_list:
        if artist not in no_albums:
            f.write(artist + '\n')