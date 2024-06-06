# Print all the edgeless nodes
# Node list is artists.txt

import pandas as pd
from colorama import Fore, Back, Style

with open('artists.txt', 'r') as f:
    artists_from_list = [line.strip() for line in f]

pd = pd.read_csv('data/edge_list.csv',on_bad_lines='skip', encoding='latin-1')

sources = set(pd['Source'].tolist())
targets = set(pd['Target'].tolist())

edgeless_nodes = set()

print("\nEdgeless nodes:\n")

for artist in artists_from_list:
    if artist not in sources and artist not in targets:
        print(Fore.YELLOW + artist)
        edgeless_nodes.add(artist)

print(Style.RESET_ALL, "\nTotal edgeless nodes: " + str(len(edgeless_nodes)))
