import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests

app = Flask(__name__)

# Check for environment variable
app.config["SQLALCHEMY_DATABASE_URI"] = "YOUR DATABASE URI"
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
db = scoped_session(sessionmaker(bind=engine))



@app.route("/login", methods=["POST", "GET"])
def login():
    """Login view"""

    # validate username and password.
    if request.method == "POST":
        u_exists = db.execute(f"SELECT COUNT(*) FROM users WHERE username='{request.form.get('username')}'")
        u_password = db.execute(f"SELECT COUNT(*) FROM users WHERE password='{request.form.get('pass')}'")
        # loop through the cursors
        for exists in u_exists:
            username = exists[0] == 1
        for pas in u_password:
            password = pas[0] == 1

        # Check if the conditions are true.
        if username and password:
            session["USERNAME"] = request.form.get("username")
            return redirect(url_for("index"))
        else:
            return "<b>username or password is incorrect.</b>"


    return render_template("login.html")



@app.route("/logout")
def logout():
    """Logout the user"""
    if session["USERNAME"] is not None:
        session["USERNAME"] = None
        return redirect(url_for("login"))



@app.route("/register", methods=["POST","GET"])
def register():
    """ Register the user """

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("pass")
        # Insert the data into the users table
        try:
            db.execute("INSERT INTO users (username, password) VALUES(:username, :password)", {"username": username, "password":password})
            db.commit()
        except:
            return "<h1>ERROR</h1>"
        return redirect(url_for("index"))
    return render_template("register.html")



@app.route("/", methods=["POST", "GET"])
def index():
    """ The Main Page"""
    # Initialize the USERNAME key if not initialized.
    try:
        # Check if the user is not logged in
        if session["USERNAME"] is None:
            # When true redirect to the login page.
            return redirect(url_for("login"))
    # Handle The KeyError
    except KeyError:
        # Initialize an empty USERNAME key value.
        session["USERNAME"] = None
        # redirect to login page.
        return redirect(url_for("login"))
    # Check if request's method is post
    if request.method == "POST":
        # getting the keyword from the search bar form.
        keyword = request.form.get("keyword")
        # getting the category from the search bar form.
        cate = request.form.get("cate")
        # Search for the keyword in the specified category.
        books = db.execute(f"SELECT isbn, title, author, year FROM books WHERE {cate} LIKE '%{keyword}%'")
        # return the result of the query.
        return render_template("index.html", books=books)
    # get the books from the books table and only show 50 books.
    # Change the LIMIt value as you please keep it low to minimize the loading proccess
    books = db.execute("SELECT isbn, title, author, year FROM books")
    return render_template("index.html", books=books)

@app.route("/isbn/<string:isbn>", methods=["GET", "POST"])
def book(isbn):
    """ Book's detail's  View"""
    # Initialize the USERNAME key if not initialized.
    try:
        # Check if the user is not logged in
        if session["USERNAME"] is None:
            # When true redirect to the login page.
            return redirect(url_for("login"))
    # Handle The KeyError
    except KeyError:
        # Initialize an empty USERNAME key value.
        session["USERNAME"] = None
        # redirect to login page.
        return redirect(url_for("login"))

    # Check if the ISBN exists if not return "DOES NOT EXISTS"
    try:
        book = db.execute(f"SELECT isbn, title, author, year FROM books WHERE isbn='{isbn}'")
    except:
        return "<h2>DOES NOT EXISTS</h2>"

    # get the comment for the book.
    reviews = db.execute(f"SELECT * FROM reviews WHERE book_isbn='{isbn}'")

    # get the average score and rating count of the book from GOODREADS APIs
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "YOUR GOODREADS APIs key", "isbns": str(isbn)})

    # extract the values from the result.
    average_rating = res.json()["books"][0]["average_rating"]
    work_ratings_count = res.json()["books"][0]["work_ratings_count"]

    # loop through the cursor to set the values.
    for isbn, title, author, year in book:
        title = title
        author = author
        year = year

    # if request metho is POST get the value of the posted comment.
    if request.method == "POST":
        comment = request.form.get("comment")

        # check the comment is not empty
        if len(comment) != 0:
            # get the user's username.
            username = session["USERNAME"]
            # insert the comment with the related data into the reviews table
            db.execute(f"INSERT INTO reviews(comment, user_name, book_isbn, timestamp) VALUES('{comment}', '{username}', '{isbn}', current_timestamp)")
            # commit the changes.
            db.commit()
            # refresh the page and show the new comment.
            return redirect(url_for("book", isbn=isbn))
    return render_template("book.html", isbn=isbn, title=title, author=author, year=year, reviews=reviews,
                            average_rating=average_rating, work_ratings_count=work_ratings_count)

@app.route("/api/<string:isbn>")
def good_reads(isbn):
    """ JSON format API of the book's detail"""
    # chech user logged in if not redirect to login page.
    if session["USERNAME"] is None:
        return redirect(url_for("login"))
    # get the missing the info of the book from the database.
    try:
        book = db.execute(f"select title, author, year, isbn from books where isbn='{isbn}'")
    except:
        return "<h2>ISBN DOES NOT EXISTS</h2>"
    for title, author, year, isbn in book:
        title = title
        author = author
        year = year
        isbn = isbn
    # get the rest of the data from API.
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "YOUR GOODREADS APIs key", "isbns": str(isbn)})
    average_rating = res.json()["books"][0]["average_rating"]
    work_ratings_count = res.json()["books"][0]["work_ratings_count"]

    # serialize the data to JSON format
    json = {
        "title": title,
        "author": author,
        "year": year,
        "isbn": isbn,
        "review_count": work_ratings_count,
        "average_score": average_rating
    }
    return json
