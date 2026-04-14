#This is where the pydantic models for FastAPI live.
#pydantic models are essentially structs from C. They contain no logic, just what fields exist in a model
from pydantic import BaseModel

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

class IngredientCreate(BaseModel):
  name: str
  quantity: float
  unit: str

