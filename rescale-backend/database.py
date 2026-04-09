#This is where we configure and have the connection to the database.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
#actual connection to database
engine = create_engine(DATABASE_URL)
#this is basically a factory that opens sessions for us when we want to access db. in endpoint scenario, we open, do work, then close.
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def getdb():
  db = SessionLocal()
  try:
    #yield is basically a return but it actually pauses rather than ending it -> hands it over to your endpoint for it to do the work, then resumes after work finishes it, severing the connection and closing it out.
    yield db
  finally:
    db.close()
