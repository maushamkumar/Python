from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserLogin
from utils import hash_password, varify_password
from models import User
from oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import schemas

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),  db: Session = Depends(get_db)):
    
    #OAuth2PasswordRequestForm = This is a class that we can use to get the username and password from the request form. 
    # It has two attributes: username and password.
    
    user = db.query(User).filter(User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not varify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # Create a token and return token 
    access_token = create_access_token(data={"user_id": user.id}) # This is data that we want to put in the payload of the token.
    
    return {"access_token": access_token, "token_type": "bearer"}





# @router.post("/login")
# def login(user_credentials: OAuth2PasswordRequestForm = Depends(),  db: Session = Depends(get_db)):
    
#     #OAuth2PasswordRequestForm = This is a class that we can use to get the username and password from the request form. 
#     # It has two attributes: username and password.
    
#     user = db.query(User).filter(User.email == user_credentials.username).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
#     if not varify_password(user_credentials.password, user.password):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
#     # Create a token and return token 
#     access_token = create_access_token(data={"user_id": user.id}) # This is data that we want to put in the payload of the token.
    
#     return {"access_token": access_token, "token_type": "bearer"}

    # bearer token and how to actually configure that on the front end. 
        
        
# @router.post("/login")
# def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == user_credentials.email).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Email")
    
#     if not varify_password(user_credentials.password, user.password):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Password")
    
    
#     return ("Login Successful")
    


# User.password = hased password
# user_credentials.password = Plane text 
