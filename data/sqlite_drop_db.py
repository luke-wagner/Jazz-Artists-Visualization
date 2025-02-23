# File: sqlite_drop_db.py
# Author: Luke Wagner
# Description:
# Drops existing sqlite database
# -------------------------------------------------------------------------------------------------

import os

from db_config import DB_FILE

try:
    os.remove(DB_FILE)
    print(f"Database file '{DB_FILE}' deleted successfully.")
except FileNotFoundError:
    print(f"Error: Database file '{DB_FILE}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")