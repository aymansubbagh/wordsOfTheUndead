# Words Of The Undead
A Book site review using goodreads APIs and covers.openlibrary.org

# requirements:
Flask
Flask-Session
psycopg2-binary
SQLAlchemy

# HOW TO USE
  in import.py file
    1 - replace "YOUR DATABASE URI" in engine = create_engine("YOUR DATABASE URI") with your own database.
    2 - then run the file from the cmd by typing python import.py

  How to get your own goodreads APIs key
    1 - Go to https://www.goodreads.com/api and sign up for a Goodreads account if you don’t already have one.
    2 - Navigate to https://www.goodreads.com/api/keys and apply for an API key. For “Application name” and “Company name” feel free to just write “project1,” and no need to 
        include an application URL, callback URL, or support URL.
    3 - You should then see your API key. (For this project, we’ll care only about the “key”, not the “secret”.)
    4 - You can now use that API key to make requests to the Goodreads API, documented here. In particular, Python code like the below
            import requests
            res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "KEY", "isbns": "9781632168146"})
            print(res.json())
# finally
  open cmd navigate to the folder and type these commands
  - set FLASK_APP=application.py # Hit Enter.
  - set FLASK_DEBUG=1 to enable debugging FLASK_DEBUG=0 to diable # Hit Enter.
  - flask run # Hit Enter.
