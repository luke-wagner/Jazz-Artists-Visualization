# Counts and outputs the number of unique albums in albums.csv

import pandas as pd
from colorama import Fore, Back, Style
import requests
from bs4 import BeautifulSoup

df = pd.read_csv('data/albums.csv',on_bad_lines='skip', encoding='latin-1')
df = df.sort_values(['Relative Link', 'Full Link', 'Artist', 'Header'], ascending=[True, True, True, True])

rel_links = set(df['Relative Link'].tolist())
full_links = set(df['Full Link'].tolist())

if (len(rel_links) - len(full_links) != 0):
    print(Fore.RED,"ERROR: NUM RELATIVE AND FULL LINKS DO NOT MATCH")
    print(Style.RESET_ALL, end='')

links_sorted = sorted(full_links)

print("Number of unique links: " + str(len(links_sorted)))
print("May not be an accurate counting of albums. Generate album_list.txt to get an accurate counting.\n")

user_input = input("Generate album_list.txt? (y/n) ")

album_titles = set()

if user_input.lower() != 'y':
    quit() # do not continue running script without user confirmation

for link in links_sorted:
    try:
        page = requests.get(link)
    except:
        print(Fore.RED,"ERROR: COULD NOT READ LINK: " + link)
        print(Style.RESET_ALL, end='')
    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find(id="firstHeading").get_text()
    album_titles.add(title)

print("\nNumber of unique albums: " + str(len(album_titles)))

with open ('album_list.txt', 'w') as f:
    for title in sorted(album_titles):
        f.write(title + '\n')