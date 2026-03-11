import sqlite3

conn = sqlite3.connect("inventory.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
id INTEGER PRIMARY KEY,
name TEXT,
stock INTEGER
)
""")

conn.commit()
conn.close()