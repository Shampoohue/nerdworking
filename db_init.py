import sqlite3

file = open("nerdworking.sql", "r", encoding='utf-8')
dbcreation = file.read()
file.close()

def get_db():
    conn = sqlite3.connect("nerdworking.db")
    conn.row_factory = sqlite3.Row
    return conn

conn = get_db()
cursor = conn.cursor()

print(dbcreation)

cursor.executescript(dbcreation)

cursor.close()
conn.close()