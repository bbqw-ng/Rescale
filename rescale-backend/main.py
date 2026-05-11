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

@app.get("/recipes/{recipe_id}")
def get_recipe_by_id(recipe_id: int, user: str = Depends(dependencies.get_current_user), db = Depends(get_db)):
  result = crud.get_recipe_by_id(db, recipe_id, user["user_id"])
  if not result:
    raise HTTPException(status_code = 404, detail = "Recipe was not found")
  return result

@app.put("/recipes/{recipe_id}")
def update_recipe(recipe: schemas.RecipeUpdate, recipe_id: int, user: str = Depends(dependencies.get_current_user), db = Depends(get_db)):
  result = crud.update_recipe(db, recipe_id, user["user_id"], recipe.name, recipe.base_servings)
  if not result:
    raise HTTPException(status_code = 404, detail = "Something went wrong with updating the recipe")
  return {"message": "Recipe successfully updated"}

@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, user: str = Depends(dependencies.get_current_user), db = Depends(get_db)):
  result = crud.delete_recipe(db, recipe_id, user["user_id"])
  if not result:
    raise HTTPException(status_code = 404, detail = "Something went wrong with deleting the recipe")
  return {"message": "Recipe deleted"}

@app.post("/recipes/{recipe_id}/ingredients")
def create_ingredient(ingredient: schemas.IngredientCreate, recipe_id: int, user: str = Depends(dependencies.get_current_user), db = Depends(get_db)):
  result = crud.create_ingredient(db, ingredient.name, ingredient.quantity, ingredient.unit, recipe_id)
  if not result:
    raise HTTPException(status_code = 500, detail = "Could not create ingredient")
  return {"message": "Ingredient creation successful"}

@app.put("/recipes/{recipe_id}/ingredients/{ingredient_id}")
def update_ingredient(ingredient: schemas.IngredientUpdate, recipe_id: int, ingredient_id: int, user: str = Depends(dependencies.get_current_user), db = Depends(get_db)):
  result = crud.update_ingredient(db, ingredient.name, ingredient.quantity, ingredient.unit, recipe_id, ingredient_id)
  if not result:
    raise HTTPException(status_code = 404, detail = "Ingredient update failed")
  return {"message": "Ingredient update successful"}

@app.delete("/recipes/{recipe_id}/ingredients/{ingredient_id}")
def delete_ingredient(recipe_id: int, ingredient_id: int, user: str = Depends(dependencies.get_current_user), db = Depends(get_db)):
  result = crud.delete_ingredient(db, ingredient_id, recipe_id)
  if not result:
    raise HTTPException(status_code = 404, detail = "Ingredient was not found")
  return {"message": "Ingredient deleted"}