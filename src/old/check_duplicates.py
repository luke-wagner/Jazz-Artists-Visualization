# Checks for duplicate lines in simple .txt file
# Prints to console when duplicates are found

filename="artists.txt"

with open(filename, 'r') as f:
    lines = f.readlines()

    lines.sort()

    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            if lines[i] == lines[j]:
                print("Duplicate found: " + lines[i])
            else:
                break