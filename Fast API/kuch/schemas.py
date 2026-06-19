from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# class post(BaseModel):
#     title: str 
#     content: str 
#     published: bool = True
    

# class CreatePost(post):
#     title: str
#     content: str
#     published: bool = True
    
# class UpdatePost(post):
#     published: bool
    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass

# class PostUpdate(PostBase):
    # pass
    
    
# class PostResponse(BaseModel):
#     title: str 
#     content: str 
#     published: bool = True
    
#     class Config:
#         orm_mode = True


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut # Here we are nesting the UserOut schema to include user details in the post response.
    
    class Config:
        orm_mode = True
        
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
        
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
    
# If we expect to send something it's best to setup a schema for that as well. 

class Token(BaseModel):
    access_token: str
    token_type: str
    

# The data we embedded into our access token. 
class TokenData(BaseModel):
    id: Optional[int] = None