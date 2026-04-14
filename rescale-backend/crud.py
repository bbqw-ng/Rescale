#CRUD stands for create, read, update, delete. this is sorta like the (restful) http layer, but is actually the backend database where the http layer is the frontend.
#sequence goes from http req -> frontend rest api -> backend crud function -> database
from model import User, Recipe, Ingredient
from sqlalchemy import Session

#User
#return: user obj with the filled attributes
def create_user(db, email, password):
  user = User(email = email, password = password)
  db.add(user)
  db.commit()
  #refreshes the object so that it generates the id for the db
  db.refresh(user)
  return user
  
def get_user_by_email(db, email):
  #gets the first user that matches email with filter, returns none if no match
  user = db.query(User).filter(User.email == email).first()
  return user

#Recipes
def create_recipe(db, name, base_servings, user_id):
  recipe = Recipe(name = name, base_servings = base_servings, user_id = user_id)
  db.add(recipe)
  db.commit()
  db.refresh(recipe)
  return recipe

def get_recipes(db, user_id):
  recipes = db.query(Recipe).filter(Recipe.user_id == user_id).all()
  return recipes

def get_recipe_by_id(db, recipe_id, user_id):
  recipe = db.query(Recipe).filter(Recipe.user_id == user_id).filter(Recipe.id == recipe_id)
  return recipe

def update_recipe(db, recipe_id, user_id, name = None, base_servings = None):
  recipeToUpdate = db.query(Recipe).filter(Recipe.user_id == user_id).filter(Recipe.id == recipe_id)
  if recipeToUpdate:
    recipeToUpdate.name = name if name else recipeToUpdate.name
    recipeToUpdate.base_servings = base_servings if base_servings else recipeToUpdate.base_servings
    db.commit()
    db.refresh(recipeToUpdate)
  return recipeToUpdate

def delete_recipe(db, recipe_id, user_id):
  recipeToDelete = db.query(Recipe).filter(Recipe.user_id == user_id).filter(Recipe.id == recipe_id)
  db.delete(recipeToDelete)
  db.commit()
  db.refresh(recipeToDelete)
  return recipeToDelete

#Ingredients
def create_ingredient(db, name, quantity, unit, recipe_id):
  ingredient = Ingredient(name = name, quantity = quantity, unit = unit, recipe_id = recipe_id)
  db.add(ingredient)
  db.commit()
  db.refresh(ingredient)
  return ingredient

def update_ingredient(db, name, quantity, unit, recipe_id, ingredient_id):
  update = db.query(Ingredient).filter(Ingredient.recipe_id == recipe_id).filter(Ingredient.id == ingredient_id)
  if update:
    #Should we do unit conversions here????? is it the databases job to do that or the layer before it?
    update.name = name if name else update.name
    update.quantity = quantity if quantity else update.quantity
    update.unit = unit if unit else update.unit
    db.commit()
    db.refresh(update)
  return update

def delete_ingredient(db, ingredient_id, recipe_id):
  delete = db.query(Ingredient).filter(Ingredient.recipe_id == recipe_id).filter(Ingredient.id == id)
  if delete:
    db.delete(delete)
    db.commit()
    db.refresh(delete)
  return delete