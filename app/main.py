from fastapi import FastAPI, HTTPException, status, Depends, Response
from pydantic import BaseModel

import psycopg2
from psycopg2.extras import RealDictCursor

from dotenv import load_dotenv
import os

from . import models
from .database import engine, get_db

from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


load_dotenv()

dbname = os.environ.get("DB_NAME")
user = os.environ.get("DB_USER")
user_pass = os.environ.get("DB_USER_PASS_PSYCOPG")
hostname = os.environ.get("DB_HOSTNAME")

connection = psycopg2.connect(database=dbname, user=user, password=user_pass, host=hostname)
cursor = connection.cursor(cursor_factory=RealDictCursor)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


# Let's try Hello World on the root dir
@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"message": "Welcome to my API"}


# Get posts
@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts(db: Session = Depends(get_db)):
    # # psycopg2 code
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    return {"all_posts": posts}


# Create posts
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # # psycopg2 code
    # cursor.execute(
    #     "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # connection.commit()

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"new_post": new_post}


# Get post by Id
@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post_id(id: int, db: Session = Depends(get_db)):
    # # psycopg2 code
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found.")
    return {"detail": post}


# Edit post by Id
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    # post_to_update = cursor.fetchone()
    # cursor.execute(
    #     "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    #     (post.title, post.content, post.published, str(id)),
    # )
    # post = cursor.fetchone()
    # connection.commit()

    post_to_update = db.query(models.Post).filter(models.Post.id == id)

    if not post_to_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found.")

    post_to_update.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"updated_post": post_to_update.first()}


# Delete post by Id
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_post(id: int, db: Session = Depends(get_db)):
    # # psycopg2 code
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    # post = cursor.fetchone()
    # cursor.execute("DELETE FROM posts WHERE id = %s", (str(id),))
    # connection.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found.")
    post.delete(synchronize_session=False)
    db.commit()
    return


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return {"data": posts}
