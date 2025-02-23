# File: sqlite_db_create.py
# Author: Luke Wagner
# Description:
# Create sqlite database to store node and edge data
# -------------------------------------------------------------------------------------------------

import sqlite3

from db_config import DB_FILE

conn = sqlite3.connect(DB_FILE)

cursor = conn.cursor()

# Read create statements from file
with open('data/create_db.sql', 'r') as f:
    create_statements = f.read().split(';')

for statement in create_statements:
    cursor.execute(statement)

conn.commit()
conn.close()

print("Database created successfully.")