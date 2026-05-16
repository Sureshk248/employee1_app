import sqlite3

conn = sqlite3.connect("employee.db")

cursor = conn.cursor()

cursor.execute("""
  CREATE TABLE IF NOT EXISTS employee (
   pernr text PRIMARY KEY NOT NULL,
   name text,
   desig text,
   dob date
  )
""")

conn.commit()
conn.close()

print("Database created")
