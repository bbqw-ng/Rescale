#This is where the pydantic models for FastAPI live.
#pydantic models are essentially structs from C. They contain no logic, just what fields exist in a model
from pydantic import BaseModel, ConfigDict

#Models
class UserCreate(BaseModel):
  email: str
  password: str

#keep these different because down the line there might be something like confirm pass 
class UserLogin(BaseModel):
  email: str
  password: str

class RecipeCreate(BaseModel):
  name: str
  base_servings: int

class RecipeUpdate(BaseModel):
  # the values here mean it is optional, could be a str or could be none
  name: str | None = None
  base_servings: int | None = None

class IngredientCreate(BaseModel):
  name: str
  quantity: float
  unit: str

class IngredientUpdate(BaseModel):
  name: str | None = None
  quantity: float | None = None
  unit: str | None = None


#We will need to write an ingredient and recipe response schema in order for
#fastapi to convert and turn it into json to use
#must have fields so we remove optionality from them

class IngredientsResponse(BaseModel):
  #pydantic needs this to know its reading from sqlalchemy obj not a regular dict
  #input schemas like the ones above dont need it because they receive plain json from frontend, but 
  #response schemas like these read from sqlalchemy model instances (objs with attributes) and not just dicts
  #this tells pydantic to expect object attributes rather than expectign a dict
  model_config = ConfigDict(from_attributes=True)
  name: str 
  quantity: float 
  unit: str  

class RecipeResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)
  name: str 
  base_servings: int 
  ingredients: list[IngredientsResponse] 

