# These are database models
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
  pass

class User(Base):
  # this is essentially declaring the name of the table
  __tablename__ = 'users'
  
  # mapped is declaring the type and mapped_column is configuring the fields options
  id = Mapped[int] = mapped_column(Integer, primary_key = True)
  email = Mapped[str] = mapped_column(String, unique = True, nullable = False)
  password = Mapped[str] = mapped_column(String, nullable = False)

  #here is a foreign key from a lower relationship
  #this enables us to not have to query every single time instead, you sqlalchemy would do it for you since it takes the recipes and since you say 
  #there is a relationship between the recipes, it will find all recipes that back populate to the owner (user) and return it.
  recipes = Mapped[list["Recipe"]] = relationship(back_populates = "owner")

class Recipe(Base):
  __tablename__ = 'recipes'

  id = Mapped[int] = mapped_column(Integer, primary_key = True)
  name = Mapped[str] = mapped_column(String, nullable = False)
  base_servings: Mapped[int] = mapped_column(Integer, nullable = False)

  #FK
  user_id = Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable = False)
  #requires this field as well for the recipe list and user to have that relationship, it uses the foriegn key which sqlalchemy automatically uses unless there are multiple. 
  owner = Mapped["User"] = relationship(back_populates = "recipes")
  #if there are multiple youd have to state which forieng key using 'forign_keys = [user_id]' in the relationship field.

class Ingredient(Base):
  __tablename__ = 'ingredients'

  id = Mapped[int] = mapped_column(Integer, primary_key = True)
  name = Mapped[str] = mapped_column(String, nullable = False)
  quantity = Mapped[float] = mapped_column(Float, nullable = False)
  #nullable when its just something like 5 entire things. just 5 cardamom.
  unit = Mapped[str] = mapped_column(String, nullable = True)
  #FK
  recipe_id = Mapped[int] = mapped_column(ForeignKey('recipes.id'))
  recipe = Mapped["Recipe"] = relationship(back_populates = "ingredients")