from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment 
load_dotenv()

app = FastAPI()

# Base model 
class post(BaseModel):
    title: str 
    content: str 
    published: bool = True

# Connect to SQL 
def create_connection():
    try: 
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            port=os.getenv("MYSQL_PORT")
        )
        if connection.is_connected():
            print("Database connected successfully")
            return connection
    except Error as e:
        print("❌ Error while connecting to MySQL:", e)
        return None
    
conn = create_connection()
cursor = conn.cursor(dictionary=True)

@app.get('/')
def root():
    return {"Message": "FastAPI code is running"}


@app.get('/posts')
def get_post():
    cursor.execute("""SELECT * FROM post""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post('/posts')
def create_post(post: post):
    cursor.execute("""
        INSERT INTO post (title, content, published)
        VALUES (%s, %s, %s)""",
        (post.title, post.content, post.published))
    
    conn.commit()

    new_id = cursor.lastrowid  # get inserted ID
    cursor.execute("SELECT * FROM post WHERE id = %s", (new_id,))
    new_post = cursor.fetchone()

    return {"data": new_post}


@app.get("/posts/{id}", status_code=status.HTTP_201_CREATED)
def get_post(id: int):
    cursor.execute("""SELECT * FROM post WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} not found"
            )
        
    # Return the post data
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int):
    # Fetch the post first (so we can return it)
    cursor.execute("SELECT * FROM post WHERE id = %s", (id,))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    # Delete the post
    cursor.execute("DELETE FROM post WHERE id = %s", (id,))
    conn.commit()

    #Return the deleted post data
    return {
        "message": "Post deleted successfully",
        "deleted_post": post
    }


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: post):
    # Update the post
    cursor.execute("""
        UPDATE post
        SET title = %s, content = %s, published = %s
        WHERE id = %s;
    """, (post.title, post.content, post.published, id))

    conn.commit()

    #  Fetch updated post
    cursor.execute("SELECT * FROM post WHERE id = %s", (id,))
    updated_post = cursor.fetchone()

    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    return {"message": "Post updated successfully", "updated_post": updated_post}

    