# File: check_duplicate_lines.py
# Author: Luke Wagner
# Description:
# Checks for duplicate lines in simple .txt file and outputs duplicates to console
# -------------------------------------------------------------------------------------------------

filename="artists.txt" # file to check

with open(filename, 'r') as f:
    # Read in lines from file and sort them
    lines = f.readlines()
    lines.sort()

    # Iterate through lines array and print duplicates
    i = 0
    while i < len(lines):
        for j in range(i+1, len(lines)):
            if lines[i] == lines[j]:
                print(f"Duplicate found: {lines[i].strip()}")
            else:
                i = j
        i += 1