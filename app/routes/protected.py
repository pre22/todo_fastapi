from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from auth.jwt import verify_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalud Auth")
    return username