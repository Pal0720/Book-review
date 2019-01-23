import csv
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session

engine = create_engine('postgresql+psycopg2://postgres:Mozart&bach3@localhost/bookly_reviews')
db = scoped_session(sessionmaker(bind=engine))

def main():
    db.execute("INSERT INTO books VALUES('1234','titles','authors',2342)")
    print("Executed")
    db.commit()

if __name__== '__main__':
    main()
