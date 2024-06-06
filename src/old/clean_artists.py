# Remove artists from artists.txt that do not have albums in albums.csv
# FINISH LATER ---------------------------------------------------------------

import pandas as pd
from colorama import Fore, Back, Style

with open('artists.txt', 'r') as f:
    artists_from_list = [line.strip() for line in f]

df = pd.read_csv('data/albums.csv',on_bad_lines='skip', encoding='latin-1')
album_artists = set(df['Artist'].tolist())

no_albums = set()

print("\nRemoving artists:\n")

for artist in artists_from_list:
    if artist not in album_artists:
        print(Fore.YELLOW + artist)
        no_albums.add(artist)

print(Style.RESET_ALL, "\nTotal artists with no albums: " + str(len(no_albums)))

user_input = input("\nOverride artists.txt? (y/n) ")

if user_input.lower() != 'y':
    quit()

with open('artists.txt', 'w') as f:
    for artist in artists_from_list:
        if artist not in no_albums:
            f.write(artist + '\n')