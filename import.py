# WARNING: only run this file to create and fill the tables
import csv

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session

# Replace With your URI
engine = create_engine("YOUR DATABASE URI")

db = scoped_session(sessionmaker(bind=engine))

def create_table():
    # Creating the required tables
    db.execute("CREATE TABLE users(username VARCHAR PRIMARY KEY, password VARCHAR NOT NULL, UNIQUE(username))")
    db.execute("CREATE TABLE books(isbn VARCHAR PRIMARY KEY, title VARCHAR NOT NULL, author VARCHAR NOT NULL, year INTEGER NOT NULL, UNIQUE(isbn))")
    db.execute("CREATE TABLE reviews(id SERIAL PRIMARY KEY, rate INTEGER NOT NULL, comment VARCHAR, user_name VARCHAR REFERENCES users, book_isbn VARCHAR REFERENCES books)")
    db.commit()


def main():
    books_csv = open("books.csv")
    reader = csv.reader(books_csv)
    # check if the Database is empty.
    is_empty = len(inspect(engine).get_table_names()) == 0

    # if empty create the tables.
    if is_empty:
        print("creating the required tables.")
        create_table()

    # loop through the csv file and add the the books
    # the books table
    for isbn,title,author,year in reader:
        print(year)
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES(:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year": int(year)})
        print(f"the book {title} by {author} published {year} with isbn:{isbn} was added.")
    db.commit()

if __name__ == "__main__":
    main()
