# File: count_albums_unique.py 
# Author: Luke Wagner
# Description:
# Counts and outputs the number of unique albums in albums.csv
# Writes list of albums to album_list.txt
# -------------------------------------------------------------------------------------------------

import pandas as pd
from colorama import Fore, Back, Style
import requests
from bs4 import BeautifulSoup
import sys
import os

# Add the parent directory to the system path; needed to import console_manager module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import console_manager # custom module for console output

# Read in album data into pandas dataframe
df = pd.read_csv('data/albums.csv',on_bad_lines='skip', encoding='latin-1')
#df = df.sort_values(['Relative Link', 'Full Link', 'Artist', 'Header'], ascending=[True, True, True, True])

# Get all relative links in albums.csv
rel_links = df['Relative Link'].tolist()
rel_links = list(set(rel_links)) # remove duplicates

# Get all full links in albums.csv
full_links = df['Full Link'].tolist()
full_links = list(set(full_links)) # remove duplicates

# Check that number of relative and full links match
# If they do not, the process for generating full links from relative links is flawed
if (len(rel_links) - len(full_links) != 0):
    console_manager.write_error("NUM RELATIVE AND FULL LINKS DO NOT MATCH")
    quit() # do not continue execution of script

# Sort list of full links
links_sorted = sorted(full_links)

# Output number of unique links
print("Number of unique links: " + str(len(links_sorted)))
print("May not be an accurate counting of albums. Generate album_list.txt to get an accurate counting.\n")

user_input = input("Generate album_list.txt? (y/n) ")

if user_input.lower() != 'y':
    quit() # do not continue running script without user confirmation

# album_titles set will hold all unique album titles
album_titles = set()

# Iterate through list of full links, get title of each album page, and add to album_titles
for link in links_sorted:
    # Get page content
    try:
        page = requests.get(link)
    except:
        console_manager.write_error("COULD NOT READ LINK: " + link)
    
    # Get title of album
    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find(id="firstHeading").get_text()

    # Add title to set
    album_titles.add(title)

# Output number of unique albums
print("\nNumber of unique albums: " + str(len(album_titles)))

# Write list of album titles to album_list.txt
with open ('album_list.txt', 'w') as f:
    for title in sorted(album_titles):
        f.write(title + '\n')