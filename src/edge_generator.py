# For each album in albums_sorted.csv, append an edge between the artist and the other personnel on the album

import csv
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style

with open('data/albums_sorted.csv', newline='') as input_file:
    reader = csv.DictReader(input_file)

    edge_dict = {}

    with open('data/edge_list.csv', 'w', newline='') as csv_file:  
        writer = csv.writer(csv_file)
        lastArtist = ""

        writer.writerow(['Source', 'Target', 'Weight'])

        for row in reader:
            if row['Artist'] != lastArtist and lastArtist != "":
                # write all edges in dict to csv
                for key, value in edge_dict.items():
                    try:
                        writer.writerow([key[0], key[1], value])
                    except:
                        print(Fore.RED, "ERROR: PROBLEM WRITING EDGE '(" + key[0] + ", " + key[1] + "): " + str(value))
                        print(Style.RESET_ALL, end="")

                edge_dict = {} # clear edge dict

            page = requests.get(row['Full Link'])
            soup = BeautifulSoup(page.content, "html.parser")

            personnel_header = soup.find('span', id='Personnel')

            if personnel_header is None:
                print(Fore.RED,"ERROR: PERSONNEL HEADER NOT FOUND")
                print(Style.RESET_ALL, end="")
                continue
            else:
                personnel_header = personnel_header.parent

            followingLists = personnel_header.find_next_siblings("ul")

            if followingLists == []:
                print(Fore.RED, "ERROR: NO LISTS FOUND")
                print(Style.RESET_ALL, end="")
                continue

            print(soup.title.string)
            print("----------------------------------------")
            for list in followingLists:
                for child in list.children:
                    people = []

                    line_text = child.text
                    sep = ' - '
                    line_text = line_text.split(sep, 1)[0] # strip everything after " - "
                    sep = '– '  
                    line_text = line_text.split(sep, 1)[0] # strip everything after " – " 
                    sep = ': '  
                    line_text = line_text.split(sep, 1)[0] # strip everything after " – " 
                    line_text = line_text.strip()

                    if ', ' in line_text:
                        # two people's names listed
                        people = line_text.split(', ')
                    elif '' == line_text:
                        continue
                    else:
                        people.append(line_text)

                    for person in people:
                        print(person)

                        if person == row['Artist']: # invalid edge
                            continue

                        # Add edge to edge list or increment weight
                        if edge_dict.get((row['Artist'], person)) == None:
                            edge_dict[(row['Artist'], person)] = 1
                        else:
                            edge_dict[(row['Artist'], person)] += 1
            print()

            lastArtist = row['Artist']

        