#JWTs live here ;x
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv


#how jwt works -> header.payload.signature
#header = algo used to create the jwt
#payload = the data inside, like the user's id or something to identify it
#signature = cryptographic proof that it has not been tampered with

#minutes until token expires.
EXPIRATION_TIME = 30
#HS256 is the standard JWT ALGO
JWT_ALGO = "HS256"
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def create_access_token(user_id : str) -> str:
  #using utcnow rather than now cuz standard jwt uses utc
  token_expiration_time = datetime.utcnow() + timedelta(minutes = EXPIRATION_TIME)
  payload = {"user_id": user_id, "exp": token_expiration_time}
  token = jwt.encode(payload, SECRET_KEY, algorithm = JWT_ALGO)
  return token








