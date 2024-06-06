# File: clean_albums.py
# Author: Luke Wagner
# Description:
# Sort albums.csv and remove duplicate lines
# -------------------------------------------------------------------------------------------------

import pandas as pd
from colorama import Fore, Back, Style
import sys

print("\nCleaning albums.csv...")
print(Fore.YELLOW, "\nWARNING: CONTENTS OF albums.csv WILL BE OVERWRITTEN")
print(Style.RESET_ALL, end='')
user_input = input("Proceed? (y/n) ",)

# If automated, remaining input will specify what to print to console
remaining_input = sys.stdin.read()
if remaining_input != '':
    remaining_input = remaining_input.strip()
    print(remaining_input)

if user_input.lower() != 'y':
    quit() # do not continue running script without user confirmation

# Read in content of albums.csv and create set of unique rows
with open('data/albums.csv', newline='') as input_file:
    lines = input_file.readlines()
    header = lines[0] # grab header from lines array, don't include in set
    unique_lines = set(lines[1:])

with open('data/albums.csv', 'w') as out_file:
    out_file.write(header.strip() + '\n') # write header

    # Write each unique line to albums.csv
    for line in unique_lines:
        line = line.strip()
        out_file.write(line + '\n')

# Use pandas to sort albums.csv
df = pd.read_csv('data/albums.csv',on_bad_lines='skip', encoding='latin-1')
df = df.sort_values(['Artist', 'Header', 'Relative Link', 'Full Link'], ascending=[True, True, True, True])

# Overwrite albums.csv with sorted dataframe
df.to_csv('data/albums.csv', index=False)