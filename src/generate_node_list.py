# Build node list
# Each node properties: Id, Importance
# Must have Id as one property, requirement for Gephi

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