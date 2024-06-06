# File: clean_albums.py
# Author: Luke Wagner
# Description:
# Sort albums.csv and remove duplicate lines
# -------------------------------------------------------------------------------------------------

import pandas as pd
import csv
import os
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

# Use pandas to sort albums.csv
df = pd.read_csv('data/albums.csv',on_bad_lines='skip', encoding='latin-1')
df = df.sort_values(['Artist', 'Header', 'Relative Link', 'Full Link'], ascending=[True, True, True, True])
df.to_csv('data/albums.csv', index=False)

# Read in content of albums.csv and create set of unique rows
with open('data/albums.csv', newline='') as input_file:
    reader = csv.DictReader(input_file)
    unique_rows = list(reader)

# Write each unique row to albums.csv
with open('data/albums.csv', 'w') as out_file:
    out_file.write('Artist,Header,Relative Link,Full Link\n') # write header

    for row in unique_rows:
        out_file.write(f'{row["Artist"]},{row["Header"]},{row["Relative Link"]},{row["Full Link"]}\n')