import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Students (
    NAME TEXT,
    CLASS TEXT,
    Marks INTEGER,
    Company TEXT
)
''')

# Insert demo data
cursor.execute("INSERT INTO Students VALUES ('Sijo', 'BTech', 75, 'JSW')")
cursor.execute("INSERT INTO Students VALUES ('Anu', 'MCom', 82, 'Infosys')")
cursor.execute("INSERT INTO Students VALUES ('Rahul', 'BSc', 90, 'Infosys')")
cursor.execute("INSERT INTO Students VALUES ('Neha', 'MTech', 95, 'Wipro')")

conn.commit()
conn.close()
