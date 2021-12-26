from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

dbname = os.environ.get("DB_NAME")
user = os.environ.get("DB_USER")
user_pass = os.environ.get("DB_USER_PASS")
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
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"all_posts": posts}


# Create posts
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    connection.commit()
    return {"new_post": new_post}


# Get post by Id
@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post_id(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found.")
    return {"detail": post}


# Edit post by Id
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post_to_update = cursor.fetchone()
    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found.")
    cursor.execute(
        "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
        (post.title, post.content, post.published, str(id)),
    )
    post = cursor.fetchone()
    connection.commit()
    return {"updated_post": post}


# Delete post by Id
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found.")
    cursor.execute("DELETE FROM posts WHERE id = %s", (str(id),))
    connection.commit()
    return
