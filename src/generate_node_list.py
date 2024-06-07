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

import console_manager # custom module for console output

print("\nGenerating node list...\n")
user_input = input("Hide console_output? (recommended) (y/n) ")

# If automated, remaining input will specify what to print to console
remaining_input = sys.stdin.read()
if remaining_input != '':
    remaining_input = remaining_input.strip()
    print(remaining_input)

if user_input.lower() == 'y':
    console_manager.console_out_off()
else:
    console_manager.console_out_on()
    print()

# required to avoid an error: https://stackoverflow.com/questions/77900971/pandas-futurewarning-downcasting-object-dtype-arrays-on-fillna-ffill-bfill
pd.set_option("future.no_silent_downcasting", True)

pytrends = TrendReq()

with open('artists.txt', 'r') as f:
    artists = [line.strip() for line in f]

# Code block 1
with open('data/node_list.csv', 'w') as f:
    f.write("Id,Importance\n")

    for artist in artists:
        querySuccessful = False
        while querySuccessful == False:
            try:
                pytrends.build_payload(kw_list=[artist], timeframe='today 5-y')
                df = pytrends.interest_over_time()
            except:
                time.sleep(1)
                continue

            querySuccessful = True

        try:
            values = df[artist].tolist()
            sum_values = sum(values)
        except:
            console_manager.write_error(str("PROBLEM READING DATA FOR: " + artist + "\n"))
            sum_values = 100

        print(df.head())
        print("\nSum of values: " + str(sum_values) + "\n")

        f.write(artist + "," + str(sum_values) + "\n")

# Code block 2
df = pd.read_csv('data/node_list.csv',on_bad_lines='skip', encoding='latin-1')
df = df.sort_values(['Importance', 'Id'], ascending=[False, True])
df.to_csv('data/node_list.csv', index=False)

# TODO: Combine code block 1 and code block 2