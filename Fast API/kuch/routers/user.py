from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from fastapi.params import Body
import models
from database import engine, get_db
from sqlalchemy.orm import Session
from schemas import  UserCreate, UserResponse
from utils import hash_password


router = APIRouter(
    prefix="/users" , 
    tags= ["Users"]  
)

@router.post("/", status_code=status.HTTP_201_CREATED,  response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Before storing the password, we need to hash it.
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=UserResponse)
def get_user(id:int, db: Session = Depends(get_db)):
    # We gonna do a quick query 
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")
    
    return user