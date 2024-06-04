import pandas as pd
import csv
import os

df = pd.read_csv('data/albums.csv',on_bad_lines='skip')
df = df.sort_values(['Artist', 'Header', 'Relative Link', 'Full Link'], ascending=[True, True, True, True])
df.to_csv('data/temp.csv', index=False)

with open('data/temp.csv', newline='') as input_file:
    reader = csv.DictReader(input_file)
    rows = list(reader)

    with open('data/albums_sorted.csv', 'w') as out_file:
        out_file.write('Artist,Header,Relative Link,Full Link\n')

        i = 0
        while i < len(rows):
            for j in range(i + 1, len(rows)):
                if j >= len(rows):
                    break
                if rows[i] != rows[j]:
                    out_file.write(f'{rows[i]["Artist"]},{rows[i]["Header"]},{rows[i]["Relative Link"]},{rows[i]["Full Link"]}\n')
                    break
                else:
                    i = j
            i += 1

os.remove('data/temp.csv')