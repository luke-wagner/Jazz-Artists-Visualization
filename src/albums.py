# File: albums.py 
# Author: Luke Wagner
# Description:
# For each artist's wiki, get a listing of their albums and each album's wiki page link.
# Write output to albums.csv
# -------------------------------------------------------------------------------------------------

import csv
import requests
from bs4 import BeautifulSoup
import sys

import console_manager # custom module for console output

print("\nFinding artist albums...\n")
user_input = input("Show console output? (recommended) (y/n) ")

# If automated, remaining input will specify what to print to console
remaining_input = sys.stdin.read()
if remaining_input != '':
    remaining_input = remaining_input.strip()
    print(remaining_input)

if user_input.lower() == 'y':
    console_manager.console_out_on()
    print()
else:
    console_manager.console_out_off()

# Read in content of artists.csv into rows array
with open('data/artists.csv', newline='') as input_file:
    reader = csv.DictReader(input_file)
    rows = list(reader)

# Loop through each row in artists.csv
with open('data/albums.csv', 'w') as out_file:
    out_file.write('Artist,Header,Relative Link,Full Link\n') # write header to albums.csv

    for row in rows:
        print("Looking at albums for: " + row['Artist'] + ' ', end='')

        page = requests.get(row['Link']) # get page content for artist's wiki
        soup = BeautifulSoup(page.content, "html.parser") # create soup obj

        # Get all headers in artist's wiki page, store to headers array
        headers = soup.find_all('h2')
        headers += soup.find_all('h3')

        album_headers = []

        # Get all headers relating to artist albums. Search for "album" or "as leader" or "as sideman"

        for header in headers:
            if 'album' in header.text.lower() or 'as leader' in header.text.lower() or 'as sideman' in header.text.lower():
                album_headers.append(header)

        # In the case no headers were found, albums may be listed under "discography"
        if album_headers == []:
            for header in headers:
                if 'discography' in header.text.lower():
                    album_headers.append(header)

        # Grab HTML blocks following each album header, breaking when we either an h2 or h3
        # One html block per album header

        followingHTMLs = []
        
        for album_header in album_headers:
            html = u""
            for element in album_header.next_siblings:
                if element.name == "h2" or element.name == "h3":
                    # end of following content
                    break
                else:
                    html += str(element)

            followingHTMLs.append(html)

        # Search HTML blocks for links, store in followingLinks
        # 2 dimensional array, each element of followingHTMLs will have a corresponding array of links in followingLinks

        followingLinks = []

        for html in followingHTMLs:
            links = [] # 1 dimensional array, all the links associated with this html block
            childSoup = BeautifulSoup(html, "html.parser") # create soup obj for this html block
            for link_item in childSoup.find_all('a'):
                link = link_item.get('href')

                if link == None:
                    continue
                
                # if album name contains ',', this will break the csv file, so replace with '®'
                link = link.replace(',', '®')

                full_link = "https://en.wikipedia.org" + link

                if "/wiki" not in link: # we only want wiki links
                    continue

                # Get link page content and check for personnel header. This indicates we have correctly
                # found an album page and not something else.

                # try/catch block to catch errors
                try:
                    link_page = requests.get(full_link)
                except:
                    console_manager.write_error(str("PROBLEM READING LINK: " + full_link))
                    continue

                # if link has personnel header, add link to links array
                link_soup = BeautifulSoup(link_page.content, "html.parser")
                headers = link_soup.find_all('h2')
                headers += link_soup.find_all('h3')
                for header in headers:
                    if 'personnel' in header.text.lower():
                        links.append(link)
                
            # after finding all links for this html block, add to followingLinks array
            followingLinks.append(links)

        # For each album header, write each album link to albums.csv
        for i in range(len(album_headers)):
            for j in range(len(followingLinks[i])):
                headerText = album_headers[i].text.replace(',', '') # remove commas
                out_file.write(f'{row["Artist"]},{headerText},{followingLinks[i][j]},https://en.wikipedia.org{followingLinks[i][j]}\n')

        print('✓')