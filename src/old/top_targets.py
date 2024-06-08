# File: top_targets.py
# Author: Luke Wagner
# Description:
# This script outputs a list of common targets in the edge list that are not in artists.txt
# Outputs to suggested_additions.txt
# -------------------------------------------------------------------------------------------------

import csv

# Read contents of edge_list.csv into rows array
with open('data/edge_list.csv', newline='') as input_file:
    reader = csv.DictReader(input_file)
    rows = list(reader)

# Read the content of artists.txt into artists array
with open('artists.txt', 'r') as f:
    artists = [line.strip() for line in f]

# targets: {artist, weight}
targets = {} # targets dict stores the combined weight of each artist as a target in the edge list

# For each edge in edge list, add weight of edge to corresponding artist in targets
for row in rows:
    target = row['Target']
    weight = int(row['Weight'])
    
    if target in targets:
        targets[target] += weight
    else:
        targets[target] = weight

# Sort targets dict by target weight
targets_sorted = sorted(targets.items(), key=lambda x:x[1],reverse=True)

# Write highest weighted targets not in artists to suggested_additions.txt
# min_weight sets minimum target weight to include in suggested_additions.txt

min_weight = 14

with open('suggested_additions.txt', 'w') as out_file:
    for target in targets_sorted:
        if target[1] >= min_weight and target[0] not in artists:
            # If first char of target is not a letter, ignore
            if target[0][0].isalpha() == False:
                continue

            # If target contains an instrument name, ignore
            if 'drums' in target[0].lower() or 'trumpet' in target[0].lower() or 'bass' in target[0].lower():
                continue
            if 'trombone' in target[0].lower() or 'saxophone' in target[0].lower() or 'piano' in target[0].lower():
                continue
            if 'flute' in target[0].lower():
                continue

            #out_file.write(target[0] + ": " + str(target[1]) + '\n')
            out_file.write(target[0] + '\n')