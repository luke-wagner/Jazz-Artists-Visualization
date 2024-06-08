# File: edgeless_nodes.py 
# Author: Luke Wagner
# Description:
# Prints out list of all edgeless nodes. Reads node list from node_list.csv
# -------------------------------------------------------------------------------------------------

import pandas as pd
from colorama import Fore, Back, Style

# Get list of all artists in node_list.csv, store to artists array
df = pd.read_csv('data/node_list.csv',on_bad_lines='skip', encoding='latin-1')
artists = df['Id'].tolist()

# Create set of all artists with at least one edge, artists_with_edges
df = pd.read_csv('data/edge_list.csv',on_bad_lines='skip', encoding='latin-1')
sources = set(df['Source'].tolist())
targets = set(df['Target'].tolist())
artists_with_edges = sources.union(targets)

edgeless_nodes = []

print("\nEdgeless nodes:\n")

# For each artist in artists, print if not in artists_with_edges
for artist in artists:
    if artist not in artists_with_edges:
        print(Fore.YELLOW + artist)
        edgeless_nodes.append(artist)

print(Style.RESET_ALL + "\nTotal edgeless nodes: " + str(len(edgeless_nodes)))
