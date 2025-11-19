from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///books.db")

with engine.connect() as con:
    results = con.execute(text("SELECT title FROM books ORDER BY title ASC"))
    for row in results:
        print(row[0])
