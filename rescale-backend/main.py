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
import dependencies
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

@app.post("/recipes")
def create_recipe(recipe: schemas.RecipeCreate, user: str = Depends(dependencies.get_current_user), db = Depends(get_db)):
  result = crud.create_recipe(db, recipe.name, recipe.base_servings, user["user_id"])
  if not result:
    #500 server failed to do something it was normally supposed to be able to do
    raise HTTPException(status_code = 500, detail = "Recipe could not be created")
  return {"message": "recipe created"}

@app.get("/recipes")
def get_recipes(user: str = Depends(dependencies.get_current_user), db = Depends(get_db)):
  result = crud.get_recipes(db, user["user_id"])
  return result

@app.get("/recipes/{id}")
def get_recipe_by_id(id: int, user: str = Depends(dependencies.get_current_user), db = Depends(get_db)):
  result = crud.get_recipe_by_id(db, id, user["user_id"])
  if not result:
    raise HTTPException(status_code = 404, detail = "Recipe was not found")
  return result

@app.put("/recipes/{id}")
def update_recipe(recipe: schemas.RecipeUpdate, id: int, user: str = Depends(dependencies.get_current_user), db = Depends(get_db)):
  result = crud.update_recipe(db, id, user["user_id"], recipe.name, recipe.base_servings)
  if not result:
    raise HTTPException(status_code = 404, detail = "Something went wrong with updating the recipe")
  return {"message": "Recipe successfully updated"}

@app.delete("/recipes/{id}")
def delete_recipe(id: int, user: str = Depends(dependencies.get_current_user), db = Depends(get_db)):
  result = crud.delete_recipe(db, id, user["user_id"])
  if not result:
    raise HTTPException(status_code = 404, detail = "Something went wrong with deleting the recipe")
  return {"message": "Recipe deleted"}
