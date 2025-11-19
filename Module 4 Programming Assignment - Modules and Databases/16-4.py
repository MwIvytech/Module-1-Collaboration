import sqlite3

con = sqlite3.connect('books.db')

cursor = con.cursor()

cursor.execute("""
               CREATE TABLE books (
               title TEXT,
               author TEXT,
               year INTEGER
)
""")

con.commit()
con.close()