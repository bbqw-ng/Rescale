from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import auth

#the param in this case is just saying which endpoint to hit in order to get a token from /docs endpoint http://localhost:8000/docs (fastapi creates this for you)
#oauth2_scheme, is just describinig the method of authentication beign used which is oauth2 with bearer tokens.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

#dependency function to verify user, should be used at every protected endpoint
def get_current_user(token: str = Depends(oauth2_scheme)):
  return auth.verify_access_token(token)