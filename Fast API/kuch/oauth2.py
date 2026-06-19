from jose import JWTError, jwt
from datetime import datetime, timedelta
from schemas import TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import database, models
from sqlalchemy.orm import Session
from typing import Optional
from config import settings


# SECRET_KEY => Ultimately handles verifying the data integrity of our token, special key that i mentioned that ultimately handles
# varifying the data integrity of our token which resides on our server only. So we're gonna have to provide that secret key. 
# ALGORITHM => The algorithm that we're gonna use to hash this token.
# EXPIRATION_TIME => How long the token is valid for.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login") # This going to be the end point of our login endpoint. 
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    
    # Here we gonna add expiration time to the token.
    # if we don't provide the expiration time, the token will be valid forever which is not good for security reason.
    # So we gonna add the expiration time to the token.
    # We can do that by adding the "exp" key to the data that we're encoding.
    # The value of the "exp" key should be the expiration time in seconds since the epoch.
    # We can use the datetime module to get the current time and add the expiration time to it.
    # We can use the timedelta module to add the expiration time to the current time.
    # Finally, we can convert the datetime object to a timestamp using the timestamp() method.
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})   
    
    encoded_jwt = jwt.encode(to_encode , SECRET_KEY, algorithm=ALGORITHM) # to_encode is payload.
    
    return encoded_jwt


# Create a function to verify the token. 
# def verify_access_token(token: str, credentials_exception):
    
#     try:
#         # user = db.query(User).filter(User.email == user_credentials.username).first()
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
#         access_token = create_access_token("user_id")
#          # auth.py field where we created token using user_id.
        
#         if id is None:
#             raise credentials_exception
#         token_data = TokenData(id=id)
#         return token_data
        
#     except JWTError as e:
#         print(e)
#         raise credentials_exception
#     except AssertionError as e:
#         print(e)


# def verify_access_token(token: str, credentials_exception):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         id: str = payload.get("user_id")  # get the field you encoded
#         if id is None:
#             raise credentials_exception
#         token_data = TokenData(id=id)
#         return token_data
#     except JWTError as e:
#         print(e)
#         raise credentials_exception
#     except AssertionError as e:
#         print(e)
#         raise credentials_exception


def verify_access_token(token: str, credentials_exception):
    try:
        print(f"Token received: {token[:50]}...") # Print first 50 chars
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Payload decoded: {payload}")
        id: str = str(payload.get("user_id"))
        if id is None:
            print("No user_id found in payload")
            raise credentials_exception
        token_data = TokenData(id=id)
        return token_data
    except JWTError as e:
        print(f"JWT Error: {e}")
        raise credentials_exception
    except Exception as e:
        print(f"Other error: {e}")
        raise credentials_exception


    
# Create a function to get the current user. 
# def get_current_user(token:str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
#     return verify_access_token(token, credentials_exception)


# We can pass this as a dependency to any of our path operations. What gonna do this take the token from the request
# automatically extract the ID for us. 
# It going to verify that the token is correct by calling the verify_access_token function.
# def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     token_data = verify_access_token(token, credentials_exception)
#     return token_data.id


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    
    return user  # Convert to int