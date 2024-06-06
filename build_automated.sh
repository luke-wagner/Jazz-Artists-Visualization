#!/bin/bash
set -e

echo "Excecuting scripts..."

# Build all the .py files in the specified order
#python src/generate_node_list.py # build out node list
python src/wikis.py # generate all artist wiki links and put in artists.csv
echo -e "y\ny\n" | python src/albums.py # for each artist, find links to all their albums and put in albums.csv
echo -e "y\ny\n" | python src/clean_albums.py # sort albums.csv and remove duplicate lines
echo -e "y\ny\n" | python src/generate_edge_list.py # generate edge list from albums.csv
echo -e "y\ny\n" | python src/clean_edge_list.py # sort edge list and remove edges to non-existent nodes

echo
echo "All scripts executed successfully!"
echo