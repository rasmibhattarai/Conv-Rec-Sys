import sqlite3
import os

db_path = "appliances.db"
sql_path = "init_db.sql"

if os.path.exists(db_path):
    os.remove(db_path)

with sqlite3.connect(db_path) as conn:
    with open(sql_path, "r") as f:
        sql_script = f.read()
    conn.executescript(sql_script)

print("Database initialized successfully.")
