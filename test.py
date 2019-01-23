# To check what does fetchone() return

# Answer : tuple with the row details

from flask import Flask, render_template, request, url_for, session, redirect
from flask_session import Session

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker



app = Flask(__name__)
app.config['SECRET_KEY'] ='Thisissupposedtobesecret!'

# Check for environment variable
#if not os.getenv("DATABASE_URL"):
#    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#Set up database
engine = create_engine("postgresql+psycopg2://postgres:Mozart&bach3@localhost/bookly_reviews")
db = scoped_session(sessionmaker(bind=engine))



user = db.execute("SELECT * FROM users WHERE name = 'Palash' AND password = 'Mozart&bach3'").fetchone()

print(user)
print(user['name'])
print(len(user))
db.close()
