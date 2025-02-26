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
import sqlite3

import console_manager # custom module for console output

print("\nFinding artist albums...\n")
user_input = input("Show console output? (recommended) (y/n) ")

# If automated, remaining input will specify what to print to console
if not sys.stdin.isatty():  # Checks if input is coming from a file/pipe
    remaining_input = sys.stdin.read().strip()
    if remaining_input:
        print(remaining_input)

if user_input.lower() == 'y':
    console_manager.console_out_on()
    print()
else:
    console_manager.console_out_off()


def get_album_headers(page_content):
    '''
    Gets h2 or h3 tags in the artist's wiki page that are likely to be album headers
    Album headers are h2 or h3 tags that likely are followed with links to album wiki pages

    Params:
    page_content: BeautifulSoup object containing artist's wiki page content

    Returns:
    album_headers: array of h2 or h3 tags
    '''
    # Get all headers in artist's wiki page, store to headers array
    headers = page_content.find_all('h2')
    headers += page_content.find_all('h3')

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

    return album_headers


def extract_html_from_album_header(header):
    '''
    Album headers are h2 or h3 tags that likely are followed with links to album wiki pages
    This function grabs the HTML content following an album header and and returns it

    Params:
    header: the h2 or h3 tag to consider

    Returns:
    html: the HTML content following the album header
    '''
    # Update as of Feb 2025, wiki page structure has changed from first version
    # This code gets the parent of the album header object, then finds the next ul element
    # This ul element may contain a list of links to album wiki pages
    html = u""
    next_element =  header.parent.findNext('ul')
    html += str(next_element)

    return html


def get_album_links(html):
    '''
    Looks at an HTML block and returns an array of links to album wiki pages in that block
    Checks for personnel header to ensure we are looking at an album page, and not some other page

    Params:
    html: the HTML content following an album header, likely containing links to album wiki pages

    Returns:
    links: an array of links to album wiki pages found in that block
    '''

    links = []

    soup = BeautifulSoup(html, "html.parser") # create soup obj for this html block
    for link_item in soup.find_all('a'):
        link = link_item.get('href')

        if link == None:
            continue
        
        # if album name contains ',', this will break the csv file, so replace with '®'
        link = link.replace(',', '®')

        full_link = "https://en.wikipedia.org" + link

        if "/wiki/" not in link: # we only want wiki links
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
                break
            
    return links

# Read in content of artists.csv into rows array
with open('data/artists.csv', newline='') as input_file:
    reader = csv.DictReader(input_file)
    rows = list(reader)

# Read artist data from artist_wikis table in database
conn = sqlite3.connect('data/main.db')
conn.row_factory = sqlite3.Row  # This makes the rows behave like dictionaries
cursor = conn.cursor()
cursor.execute("SELECT * FROM artists")
rows = [dict(row) for row in cursor.fetchall()]

# Loop through each row in artists.csv
with open('data/albums.csv', 'w') as out_file:
    out_file.write('Artist,Header,Relative Link,Full Link\n') # write header to albums.csv

    for row in rows:
        print("Looking at albums for: " + row["artist_name"] + ' ', end='')

        # See if albums have already been found for this artist
        # script_progress table keeps record of which artists for this process have already been searched
        conn = sqlite3.connect('data/main.db')
        cursor = conn.cursor()
        try:
            cursor.execute(f'''
            SELECT * FROM script_progress
            WHERE process_identifier = 'ARTIST_ALBUMS_FETCHED'
            AND key = '{row["artist_name"]}'
            AND value = 1 -- 1 indicates process completed
            ''')
            result = cursor.fetchone()
        except:
            console_manager.write_error(str("PROBLEM READING SCRIPT_PROGRESS TABLE"))
        
        if result != None:
            print('✓\n- Albums already catalogued for this artist')
            continue

        page = requests.get(row["link"]) # get page content for artist's wiki
        soup = BeautifulSoup(page.content, "html.parser") # create soup obj

        # Get album headers for this artist
        # Album headers are h2 or h3 tags that likely are followed with links to album wiki pages
        album_headers = get_album_headers(soup)

        # For each album header, look in the html following for links to album pages
        # If an album page is found, write it to albums.csv (or insert into albums table)
        for header in album_headers:
            html = extract_html_from_album_header(header)
            links = get_album_links(html)

            for link in links:
                headerText = header.text.replace(',', '') # remove commas

                # Write to csv
                out_file.write(f'{row["artist_name"]},{headerText},{link},https://en.wikipedia.org{link}\n')

                # Also insert into albums table
                conn = sqlite3.connect('data/main.db')
                cursor = conn.cursor()

                try:
                    cursor.execute(f'''
                    INSERT INTO albums (artist_name, header, rel_link, full_link)
                    VALUES ('{row["artist_name"]}', '{headerText}', '{link}', 'https://en.wikipedia.org{link}')
                    ''')
                except sqlite3.IntegrityError: # album already exists
                    pass

                conn.commit()
                conn.close()
        
        # Once artist has been handled entirely, insert into script_progress table to indicate completion
        # On next run, this artist will not be reprocessed
        conn = sqlite3.connect('data/main.db')
        cursor = conn.cursor()
        cursor.execute(f'''
        INSERT INTO script_progress (script_name, process_identifier, key, value)
        VALUES ('albums.py', 'ARTIST_ALBUMS_FETCHED', '{row["artist_name"]}', '1')
        ''')
        conn.commit()
        conn.close()
        print('✓')