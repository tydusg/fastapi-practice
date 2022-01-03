from fastapi import FastAPI, HTTPException, status, Depends, Response

from dotenv import load_dotenv
import os

from . import models
from .database import engine, get_db
from . import schemas

from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

load_dotenv()

dbname = os.environ.get("DB_NAME")
user = os.environ.get("DB_USER")
user_pass = os.environ.get("DB_USER_PASS_PSYCOPG")
hostname = os.environ.get("DB_HOSTNAME")

app = FastAPI()


# Get posts
@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# Create posts
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Get post by Id
@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post_id(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found.")
    return post


# Edit post by Id
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found.")
    post.update(post.dict(), synchronize_session=False)
    db.commit()
    return post.first()


# Delete post by Id
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found.")
    post.delete(synchronize_session=False)
    db.commit()
    return
