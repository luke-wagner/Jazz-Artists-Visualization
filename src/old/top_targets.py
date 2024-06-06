# This script outputs a list of common targets in the edge list that are not in top_100.txt

import csv

# Open the sorted edge list CSV file
with open('data/edges_sorted.csv', newline='') as input_file:
    reader = csv.DictReader(input_file)

    # Read the top 100 artists from the top_100.txt file
    with open('top_100.txt', 'r') as f:
        top_100 = [line.strip() for line in f]

    # TODO: Create a dict, "targets" to store the combined weight of each artist as a target in the edge list
    targets = {}

    for row in reader:
        target = row['Target']
        weight = int(row['Weight'])
        
        if target in targets:
            targets[target] += weight
        else:
            targets[target] = weight

    targets_sorted = sorted(targets.items(), key=lambda x:x[1],reverse=True)
    
    with open('suggested_additions.txt', 'w') as out_file:
        for target in targets_sorted:
            if target[1] > 15 and target[0] not in top_100:
                out_file.write(target[0] + '\n')