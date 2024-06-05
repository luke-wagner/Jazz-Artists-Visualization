# For each edge in the edge list, if target is not in artists.txt, remove edge

import csv

with open('artists.txt', 'r') as f:
    artists_from_list = [line.strip() for line in f]

with open('data/edges_sorted.csv', newline='') as input_file:
    reader = csv.DictReader(input_file)

    with open('data/edge_list_clean.csv', 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row in reader:
            if row['Target'] not in artists_from_list:
                continue
            else:
                writer.writerow(row)