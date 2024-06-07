# This script outputs a list of common targets in the edge list that are not in artists.txt

import csv

# Open the sorted edge list CSV file
with open('data/edge_list.csv', newline='') as input_file:
    reader = csv.DictReader(input_file)

    # Read the artists from artists.txt into an array
    with open('artists.txt', 'r') as f:
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
            if target[1] > 13 and target[0] not in top_100 and target[0][0].isalpha():
                if 'drums' in target[0].lower() or 'trumpet' in target[0].lower() or 'bass' in target[0].lower():
                    continue
                if 'trombone' in target[0].lower() or 'saxophone' in target[0].lower() or 'piano' in target[0].lower():
                    continue
                if 'flute' in target[0].lower():
                    continue

                #out_file.write(target[0] + ": " + str(target[1]) + '\n')
                out_file.write(target[0] + '\n')