from fastapi import FastAPI
from database import engine
from model import Base

app = FastAPI()

#reads model, creates respective tables if they dont exist, binds it to database connection.
Base.metadata.create_all(bind = engine)

@app.get("/")
def root():
  return {"message": "api is running correctly"}