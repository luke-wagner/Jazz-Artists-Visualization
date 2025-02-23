# File: generate_node_list.py
# Author: Luke Wagner
# Description:
# For each artist in artists.txt, create a node in node_list.csv
#
# Node properties: Id, Importance
# Id: Artist name ("Id" is a required property for nodes in Gephi)
# Importance: Google search popularity based on pytrends data from the last 5 years
# -------------------------------------------------------------------------------------------------

from pytrends.request import TrendReq
import pandas as pd
from colorama import Fore, Back, Style
import time
import sys
import sqlite3

import console_manager # custom module for console output

print("\nGenerating node list...\n")
user_input = input("Hide console_output? (recommended) (y/n) ")

# If automated, remaining input will specify what to print to console
if not sys.stdin.isatty():  # Checks if input is coming from a file/pipe
    remaining_input = sys.stdin.read().strip()
    if remaining_input:
        print(remaining_input)

if user_input.lower() == 'y':
    console_manager.console_out_off()
else:
    console_manager.console_out_on()
    print()

# Required to avoid an error: https://stackoverflow.com/questions/77900971/pandas-futurewarning-downcasting-object-dtype-arrays-on-fillna-ffill-bfill
pd.set_option("future.no_silent_downcasting", True)

# Create pytrends object
pytrend_obj = TrendReq()

# Read artists from artists.txt into artists array
with open('artists.txt', 'r') as f:
    artists = [line.strip() for line in f]

# Query db for existing nodes, only get trend data for new nodes
conn = sqlite3.connect('data/main.db')
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT artist_name FROM node_list")
existing_nodes = cursor.fetchall()
conn.close()

# Remove existing nodes from artists array
for node in existing_nodes:
    artists.remove(node[0])

print("New nodes to add: " + str(len(artists)) + "\n")

node_list = {} # use dict to store nodes and node info

# Loop over each artist, and store their name and importance to the node_list dict
loop_counter = 0 # keep track of how many times we've looped
for artist in artists:
    # Keep trying to get data until we query is successful
    querySuccessful = False
    while querySuccessful == False:
        try:
            # get trend data, store to pandas dataframe, df
            pytrend_obj.build_payload(kw_list=[artist], timeframe='today 5-y')
            df = pytrend_obj.interest_over_time()
        except:
            time.sleep(1)
            continue

        querySuccessful = True

    # Trends data is stored in df, try to extract the sum of values
    try:
        values = df[artist].tolist()
        sum_values = sum(values)
    except:
        console_manager.write_error(str("PROBLEM READING DATA FOR: " + artist + "\n"))
        sum_values = 100 # give a default importance value of 100 for this artist

    # For debugging
    print(df.head())
    print("\nSum of values: " + str(sum_values) + "\n")

    # Add entry to node_list, use loop counter as dict key
    node_list[loop_counter] = [artist, sum_values]

    loop_counter += 1

# Node list built, now use df to sort by importance then write to node_list.csv
df = pd.DataFrame.from_dict(node_list, orient='index', columns=['Id','Importance'])
df = df.sort_values(['Importance', 'Id'], ascending=[False, True])

# Write to csv file
df.to_csv('data/node_list.csv', index=False)

# In addition to writing to csv file, insert rows into sqlite db (node_list table)
# Once sqlite db is fully functional, csv functionality will be deleted #TODO
conn = sqlite3.connect('data/main.db')

cursor = conn.cursor()

for index, row in df.iterrows():
    cursor.execute("INSERT INTO node_list (artist_name, importance) VALUES (?, ?)", (row['Id'], row['Importance']))

conn.commit()
conn.close()