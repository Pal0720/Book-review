import os
from flask import Flask, render_template, request, url_for, session, redirect
from flask_session import Session

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from helpers import *

import json
import requests

app = Flask(__name__)



# Check for environment variable
#if not os.getenv("DATABASE_URL"):
#    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] ='Thisissupposedtobesecret!'
Session(app)

#Set up database
engine = create_engine("postgresql+psycopg2://postgres:Mozart&bach3@localhost/bookly_reviews")
db = scoped_session(sessionmaker(bind=engine))



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup",methods=['POST','GET'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        username = request.form.get('username')
        email = request.form.get("email")
        password = request.form.get("password")

        db.execute("INSERT INTO users(name, email, password) VALUES (:username, :email, :password)",{"username":username,"email":email, "password":password})
        db.commit()
        session["username"] = username
        session['email'] = email

        return redirect(url_for("index"))

@app.route("/login",methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.execute("SELECT * FROM users WHERE name = :username AND password = :password",{"username":username, "password":password}).fetchone()
        db.close()
        if user is not None:
            session['username'] = user['name']
            session['email'] = user['email']
            return render_template("index.html")
        else:
            return '<h2> Incorrect username or password. Please try again </h2>'
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('username')
    return render_template("index.html")


@app.route("/search", methods=['POST'])
def search():
    if request.method == 'POST':
        book = request.form.get('searchbar')
        book = "%" + book + "%"
        book_search = db.execute("SELECT * FROM books WHERE isbn LIKE :book OR title LIKE :book OR author LIKE :book", {"book":book}).fetchall()
        result_list = []
        for result in book_search:
            result_list.append(result)
        if book_search is not None:
            return render_template("search.html", result_list=result_list)
        else:
            return "<h2> No such book. Please try again </h2>"


@app.route("/book/<isbn>", methods = ["POST", "GET"])
def book(isbn):
    if request.method == "POST":
        rating = request.form.get("rating")
        review_text = request.form.get("review-text")
        db.execute("INSERT INTO reviews(reviewer, book, rating ,review_text) VALUES (:reviewer, :book, :rating, :review_text)", {"reviewer":session['username'], "book":isbn, "rating":rating, "review_text":review_text })
        db.commit()
        return redirect(url_for("book",isbn = isbn))
    else:

        result = get_review_counts(isbn)
        reviews = db.execute("SELECT * FROM reviews WHERE book = :isbn", {"isbn":isbn}).fetchall()
        book_search = db.execute("SELECT * FROM books WHERE isbn = :isbn", { "isbn":isbn }).fetchone()
        return render_template("book.html", book_search=book_search, reviews = reviews, result =result)

@app.route("/api/<isbn>")
def api(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":'omv1Rp72n1GcXXHuWBCw', "isbns": isbn})
    json_data = res.json()
    return render_template("api.html", json_data = json_data)




if __name__ == '__main__':
    app.run(debug=True)
