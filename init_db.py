import sqlite3

connection = sqlite3.connect('college_tms.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()

print("Database initialized successfully!")
