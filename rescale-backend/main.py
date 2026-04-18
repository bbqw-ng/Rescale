from fastapi import FastAPI
from database import engine
from model import Base
from passlib.hash import bcrypt
from fastapi import Depends, HTTPException
from database import get_db
from jose import jwt
import os
from dotenv import load_dotenv
import crud
import schemas
import auth

SECRET_KEY = os.getenv("SECRET_KEY")
app = FastAPI()

#reads model, creates respective tables if they dont exist, binds it to database connection.
Base.metadata.create_all(bind = engine)

@app.get("/")
def root():
  return {"message": "api is running correctly"}

@app.post("/register")
#Depends is FastApi's way of injecting database sessions
def register(user: schemas.UserCreate, db = Depends(get_db)):
  #process -> deconstruct the schema, with the email and pass, hash the pass to protect it in the database
  if crud.get_user_by_email(db, user.email):
    #Failure response code 400
    raise HTTPException(status_code = 400, detail = "Email is already registered")
  else:
    hashed_password = bcrypt.hash(user.password)
    crud.create_user(db, user.email, hashed_password)
  return {"message": "account created"}

@app.post("/login")
def login(user: schemas.UserLogin, db = Depends(get_db)):
  #take the pydantic model, deconstruct it, verify that email exists, verify password hash, generate jwt token return token.
  result = crud.get_user_by_email(db, user.email)
  if not result:
    raise HTTPException(status_code = 401, detail = "Invalid email or password")
    #verify (plain password, hashed password) hashed = database one, plain = provided
  if not bcrypt.verify(user.password, result.password):
    raise HTTPException(status_code = 401, detail = "Invalid email or password")
  #create jwt token and send back along with success message 
  token = auth.create_access_token(result.id)
  return {"access_token": token, "token_type": "bearer"}
  

  