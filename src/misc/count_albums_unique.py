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

print("Number of unique albums: " + str(len(links_sorted)))

user_input = input("Generate album_list.txt? (y/n) ")

if user_input.lower() != 'y':
    quit()

with open ('album_list.txt', 'w') as f:
    for link in links_sorted:
        try:
            page = requests.get(link)
        except:
            print(Fore.RED,"ERROR: COULD NOT READ LINK: " + link)
            print(Style.RESET_ALL, end='')
        soup = BeautifulSoup(page.content, "html.parser")
        title = soup.find(id="firstHeading").get_text()
        f.write(title + '\n')