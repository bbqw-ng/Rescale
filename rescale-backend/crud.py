#CRUD stands for create, read, update, delete -> this is the backend layer, restful is the frontend http layer
#sequence goes from http req -> frontend rest api -> backend crud function -> database
from model import User, Recipe, Ingredient
from sqlalchemy.orm import Session

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
  recipe = db.query(Recipe).filter(Recipe.user_id == user_id, Recipe.id == recipe_id).first()
  return recipe

def update_recipe(db, recipe_id, user_id, name = None, base_servings = None):
  recipe = db.query(Recipe).filter(Recipe.user_id == user_id, Recipe.id == recipe_id).first()
  if recipe:
    recipe.name = name if name else recipe.name
    recipe.base_servings = base_servings if base_servings else recipe.base_servings
    db.commit()
    db.refresh(recipe)
  return recipe

def delete_recipe(db, recipe_id, user_id):
  recipe = db.query(Recipe).filter(Recipe.user_id == user_id, Recipe.id == recipe_id).first()
  if recipe:
    db.delete(recipe)
    db.commit()
  return recipe

#Ingredients
def create_ingredient(db, name, quantity, unit, recipe_id):
  ingredient = Ingredient(name = name, quantity = quantity, unit = unit, recipe_id = recipe_id)
  db.add(ingredient)
  db.commit()
  db.refresh(ingredient)
  return ingredient

def update_ingredient(db, name, quantity, unit, recipe_id, ingredient_id):
  ingredient = db.query(Ingredient).filter(Ingredient.recipe_id == recipe_id, Ingredient.id == ingredient_id).first()
  if ingredient:
    #we dont do unit conversion here because it is not the database's job
    ingredient.name = name if name else ingredient.name
    ingredient.quantity = quantity if quantity else ingredient.quantity
    ingredient.unit = unit if unit else ingredient.unit
    db.commit()
    db.refresh(ingredient)
  return ingredient

def delete_ingredient(db, ingredient_id, recipe_id):
  ingredient = db.query(Ingredient).filter(Ingredient.recipe_id == recipe_id, Ingredient.id == ingredient_id).first()
  if ingredient :
    db.delete(ingredient)
    db.commit()
  return ingredient