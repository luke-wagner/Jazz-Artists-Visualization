#!/bin/bash
set -e

echo "Clearing database..."

# Drop and recreate the database
python data/sqlite_drop_db.py
python data/sqlite_db_create.py