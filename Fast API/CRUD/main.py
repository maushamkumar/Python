from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from random import randrange


app = FastAPI()

class post(BaseModel):
    title: str
    content: str

my_post = [{"title": "First Post", "content": "This is my first post", "id": 1}, 
           {"title": "Second Post", "content": "This is my second post", "id": 2}] 

        
@app.get("/")
def root():
    return {"message": "Kuch toh kar raha hu code suggest mat karo"}


@app.get("/posts")
def get_post():
    return {"data": my_post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_user(post: post):
    # Title, content and id
    print(post.title)
    print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = randrange(1, 100000)
    my_post.append(post_dict)
    return {"data": post_dict}


def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p
        
def find_post_index(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i 
        
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with id {id} not fond")
    return {"data": post}
    
    
@app.delete('/posts/{id}')
def delete_post(id: int):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with id {id} not found")
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post:post):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with id {id} not found")
    post_dict = post.dict()
    post_dict['id'] = id
    post_dict[index] = post_dict
    return {"data": post_dict}
    

    