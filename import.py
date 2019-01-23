import os
import csv
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session

engine = create_engine("postgresql+psycopg2://postgres:Mozart&bach3@localhost/bookly_reviews")
db = scoped_session(sessionmaker(bind=engine))

def main():
 count = 0
 with open("books.csv") as f:
     read = csv.reader(f)
     next(read)

     for isbn, title, author, year in read:
         db.execute("INSERT INTO books(isbn,title,author,year) VALUES (:isbn,:title,:author,:year)",{"isbn":isbn,"title":title,"author":author,"year":year})
         count += 1
     db.commit()
     print ("Execution complete. Total count is {}".format(count))


if __name__ == '__main__':
    main()
