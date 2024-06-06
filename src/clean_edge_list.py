# Sort edge list and for each edge in the edge list, if target is not in artists.txt, remove edge

import csv
from colorama import Fore, Back, Style
import pandas as pd
import sys

print("\nCleaning edge list...")
print(Fore.YELLOW, "\nWARNING: CONTENTS OF edge_list.csv WILL BE OVERWRITTEN")
print(Style.RESET_ALL, end='')
user_input = input("Proceed? (y/n) ",)

# If automated, remaining input will specify what to print to console
remaining_input = sys.stdin.read()
if remaining_input != '':
    remaining_input = remaining_input.strip()
    print(remaining_input)

if user_input.lower() != 'y':
    quit()

df = pd.read_csv('data/edge_list.csv',on_bad_lines='skip', encoding='latin-1')
df = df.sort_values(['Weight', 'Source', 'Target'], ascending=[False, True, True])
df.to_csv('data/edge_list.csv', index=False)

with open('artists.txt', 'r') as f:
    artists_from_list = [line.strip() for line in f]

with open('data/edge_list.csv', newline='') as input_file:
    reader = csv.DictReader(input_file)
    rows = list(reader)

with open('data/edge_list.csv', 'w', newline='') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)
    writer.writeheader()

    for row in rows:
        if row['Target'] not in artists_from_list:
            continue
        else:
            writer.writerow(row)