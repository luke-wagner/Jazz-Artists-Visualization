# File: sqlite_db_create.py
# Author: Luke Wagner
# Description:
# Create sqlite database to store node and edge data
# -------------------------------------------------------------------------------------------------

import sqlite3

from db_config import DB_FILE

conn = sqlite3.connect(DB_FILE)

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE node_list (
        artist_name TEXT PRIMARY KEY NOT NULL,
        importance INT
    );
''')

conn.commit()
conn.close()

print("Database created successfully.")