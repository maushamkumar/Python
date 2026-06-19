from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from database import engine, get_db
from sqlalchemy.orm import Session
from schemas import  PostCreate, PostResponse
from typing import Optional
import models
import oauth2


router = APIRouter(
    prefix="/posts",
    tags= ["Posts"] 
)

models.Base.metadata.create_all(bind=engine)




@router.get("/", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db), 
              current_user_id: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    # # This is for retrieving all the posts from the database.
    # post = db.query(models.Post).all()
    
    
    # But if you want to retrieve posts only for the currently logged in user, you can do this:
    # post = db.query(models.Post).filter(models.Post.owner_id == current_user_id.id).limit(limit).offset(skip).all()
    
    post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    
    return post



# @router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
# def create_post(post: PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user) ): # user_id:int=Depends(get_current_user)
#     print(user_id)
#     # new_post = models.Post(title=post.title, content=post.content, published=post.published)
#     new_post = models.Post(**post.dict()) # This is same as the above line.
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
    
#     return new_post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):
    # print(f"Current user ID: {user_id}")
    # print(user_id.id)
    new_post = models.Post(owner_id = current_user_id.id, **post.dict())  # Remove owner_id=current_user_id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get("/{id}", response_model=PostResponse)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return  post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):
    
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    
    post = deleted_post.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    if post.owner_id != current_user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):
    
    index = db.query(models.Post).filter(models.Post.id == id)
    # index = find_index_post(id)
    post = index.first()
    
    if index.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    if post.owner_id != current_user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    index.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    # post_dict['id'] = id 
    # my_post[index] = post_dict
    return index.first()