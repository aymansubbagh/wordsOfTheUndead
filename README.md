# Words Of The Undead
A Book site review using goodreads APIs and covers.openlibrary.org

# requirements:
Flask</br>
Flask-Session</br>
psycopg2-binary</br>
SQLAlchemy

# HOW TO USE
  in import.py file</br>
    1.  replace "YOUR DATABASE URI" in `engine = create_engine("YOUR DATABASE URI")` with your own database.</br>
    2.  then run the file from the cmd by typing python import.py </br>

  How to get your own goodreads APIs key</br>
    1.  Go to https://www.goodreads.com/api and sign up for a Goodreads account if you don’t already have one.</br>
    2.  Navigate to https://www.goodreads.com/api/keys and apply for an API key. For “Application name” and “Company name” feel free to just write “project1,” and no need to 
        include an application URL, callback URL, or support URL.</br>
    3.  You should then see your API key. (For this project, we’ll care only about the “key”, not the “secret”.)</br>
    4.  You can now use that API key to make requests to the Goodreads API, documented here. In particular, Python code like the below</br>
            ```
            import requests
            res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "KEY", "isbns": "9781632168146"})
            print(res.json())
            ```</br>
    finally</br>
      open cmd navigate to the folder and type these commands</br>
      1. set FLASK_APP=application.py # Hit Enter.</br>
      2. set FLASK_DEBUG=1 to enable debugging FLASK_DEBUG=0 to diable # Hit Enter.</br>
      3. flask run # Hit Enter.</br>
# Screenshots
![signin](/static/images/signin.png)
![register](/static/images/register.png)
![home](/static/images/home.png)
![book](/static/images/book.png)
