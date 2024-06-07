# File: generate_edge_list.py
# Author: Luke Wagner
# Description:
# For each album in albums.csv, create an edge between the source artist and each other personnel member on the album
# Write output to edge_list.csv
# -------------------------------------------------------------------------------------------------

import csv
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
import sys

import console_manager # custom module for console output

###################################################################################################
# HELPER FUNCTIONS:
# -------------------------------------------------------------------------------------------------
# Writes edge_dict to csv file using the provided writer
def write_edges(edge_dict, writer):
    for key, value in edge_dict.items():
        # May throw error when trying to write special characters
        try:
            writer.writerow([key[0], key[1], value])
        except:
            console_manager.write_error(str("PROBLEM WRITING EDGE '(" + key[0] + ", " + key[1] + "): " + str(value)))

# -------------------------------------------------------------------------------------------------
# Tries to get personnel header from soup object. If found returns header, otherwise returns None
def get_personnel_header(soup_obj):
    # Try to find personnel header
    personnel_header = soup_obj.find('span', id='Personnel')

    if personnel_header is None:
        return None
    else:
        personnel_header = personnel_header.parent # we don't want the span tag, rather its parent
    
    return personnel_header

# -------------------------------------------------------------------------------------------------
# Returns list of people from a line of text by removing common surrounding text and then splicing by comma
def people_from_line_text(line_text):
    people = [] # create empty list of people's names

    # remove common text following artist's name in li tag
    sep = ' - '
    line_text = line_text.split(sep, 1)[0] # strip everything after " - "
    sep = '– '  
    line_text = line_text.split(sep, 1)[0] # strip everything after " – " 
    sep = ': '  
    line_text = line_text.split(sep, 1)[0] # strip everything after ": " 
    line_text = line_text.strip()

    # Sometimes more than one collaborators are listed on the same line
    # In this case, split the line by comma and then append each name to the people array
    if ', ' in line_text:
        people = line_text.split(', ')
    elif '' == line_text:
        return people # ignore empty lines
    else:
        # people will only contain one name, but we must keep it as a list for consistency
        people.append(line_text) 

    return people
###################################################################################################

print("\nGenerating edge list...\n")
user_input = input("Hide console output? (recommended) (y/n) ")

# If automated, remaining input will specify what to print to console
remaining_input = sys.stdin.read()
if remaining_input != '':
    remaining_input = remaining_input.strip()
    print(remaining_input)

if user_input.lower() == 'y':
    console_manager.console_out_off()
else:
    console_manager.console_out_on()

with open('data/albums.csv', newline='') as input_file:
    reader = csv.DictReader(input_file) # create reader object for albums.csv
    rows = list(reader)

edge_dict = {}

with open('data/edge_list.csv', 'w', newline='') as csv_file:  
    writer = csv.writer(csv_file)
    lastArtist = ""

    writer.writerow(['Source', 'Target', 'Weight']) # write header for edge_list.csv

    # Loop through each row in albums.csv
    for row in rows:
        # We only want to write to edge_list.csv when the artist we are looking at changes
        # This will prevent writing duplicate edges each of weight 1
        currentArtist = row['Artist']
        if currentArtist != lastArtist and lastArtist != "":
            # We are looking at a new artist, write existing edge_dict to edge_list.csv
            write_edges(edge_dict, writer)
            edge_dict = {} # clear edge dict

        # ---------------------------------------------------------------------------------------
        # Get page content for album's wiki page
        # Use this to look for personnel on album
        # ---------------------------------------------------------------------------------------
        page = requests.get(row['Full Link']) # get page content
        soup = BeautifulSoup(page.content, "html.parser") # create soup obj
        album_title = soup.title.string.replace(" - Wikipedia", "") # infer album title from html

        # Get personnel header
        personnel_header = get_personnel_header(soup)
        if personnel_header is None:
            console_manager.write_error(str("PERSONNEL HEADER NOT FOUND FOR ALBUM: " + album_title))
            continue

        # Personnel members names are usually list items in an unordered list
        # Therefore, we must find all lists following the personnel header
        followingLists = personnel_header.find_next_siblings("ul")
        if followingLists == []:
            console_manager.write_error(str("NO PERSONNEL LISTS FOUND FOR ALBUM: " + album_title))
            continue

        # Print album title (useful for debugging)
        print(album_title)
        print("----------------------------------------")
        for list in followingLists:
            # Loop over list items in each following list. Should contain people's names. These are the collaborators of the album
            for list_item in list.children:
                line_text = list_item.text # get text from list item

                people = people_from_line_text(line_text) # personnel array for this list
                if len(people) == 0: # could happen with empty line
                    continue

                for person in people:
                    print(person) # for debugging

                    if person == row['Artist']: # don't allow loops in edge list
                        continue

                    # Add edge to edge list or if it already exists, increment its weight
                    if edge_dict.get((row['Artist'], person)) == None:
                        edge_dict[(row['Artist'], person)] = 1
                    else:
                        edge_dict[(row['Artist'], person)] += 1
        print()

        lastArtist = row['Artist'] # set last artist to current artist for next iteration

