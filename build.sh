#!/bin/bash
set -e

# Build all the .py files in the specified order
#python src/wikis.py
#python src/albums.py
#python src/album_sorter.py
#python src/edge_generator.py
python src/edge_sorter.py

echo
echo "All scripts executed successfully!"
echo