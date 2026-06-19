from routers import post, user, auth
from fastapi import FastAPI, HTTPException, Response, status, Depends
from database import engine
from dotenv import load_dotenv
import models
import os


# Load environment variables from .env
load_dotenv()

models.Base.metadata.create_all(bind=engine)
app = FastAPI()



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)