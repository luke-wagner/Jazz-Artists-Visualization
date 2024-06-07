# File: clean_edge_list.py
# Author: Luke Wagner
# Description:
# Sorts edge list, then for each edge, if target of edge is not in artists.txt, removes edge
# The point of this is to remove edges to non-existent nodes
# -------------------------------------------------------------------------------------------------

import csv
from colorama import Fore, Back, Style
import pandas as pd
import sys

import console_manager # custom module for console output

print("\nCleaning edge list...")
console_manager.write_warning("CONTENTS OF edge_list.csv WILL BE OVERWRITTEN")
user_input = input("Proceed? (y/n) ",)

# If automated, remaining input will specify what to print to console
remaining_input = sys.stdin.read()
if remaining_input != '':
    remaining_input = remaining_input.strip()
    print(remaining_input)

if user_input.lower() != 'y':
    quit() # do not continue running script without user confirmation

# Use pandas to sort edge_list.csv
df = pd.read_csv('data/edge_list.csv',on_bad_lines='skip', encoding='latin-1')
df = df.sort_values(['Weight', 'Source', 'Target'], ascending=[False, True, True])
df.to_csv('data/edge_list.csv', index=False)

# Read artists from artists.txt into artists array
with open('artists.txt', 'r') as f:
    artists_from_list = [line.strip() for line in f]

# Read contents of edge_list.csv into rows array
with open('data/edge_list.csv', newline='') as input_file:
    reader = csv.DictReader(input_file)
    rows = list(reader)

with open('data/edge_list.csv', 'w', newline='') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)
    writer.writeheader() # write header for edge_list.csv

    # For each element in rows, if target is in artists_from_list, write row to edge_list.csv
    for row in rows:
        if row['Target'] not in artists_from_list:
            continue # target is not in artists_from_list, ignore this edge
        else:
            writer.writerow(row) # write row to edge_list.csv