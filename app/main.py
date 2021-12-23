from typing import Optional
from fastapi import FastAPI, Response, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


# Okay, so here's the plan:
# Post structure
#   id
#   title
#   content
#   published
#   created_at
# Dummy list of posts
my_posts = [
    {
        "id": 1,
        "title": "First Post",
        "content": "This is the first post ever in this API.",
        "published": True,
        "created_at": "2021-12-23 14:50:26.159446",
    },
    {
        "id": 2,
        "title": "Second Post",
        "content": "Okay. So this here's the second post. You got that?",
        "published": True,
        "created_at": "2021-12-23 14:53:47.437648",
    },
]


def get_post_by_id(id):
    for post in my_posts:
        if post["id"] == id:
            return post


class Post(BaseModel):
    id: int = None
    title: str
    content: str
    published: bool = True
    created_at: Optional[str]


# Let's try Hello World on the root dir
@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"message": "Welcome to my API"}


# Get posts
@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts():
    return {"all_posts": my_posts}


# Create posts
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    new_post = post.dict()
    my_posts.append(new_post)
    return {"new_post": new_post}


# Get post by Id
@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post_id(id: int):
    post = get_post_by_id(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found.")
    return {"post_detail": post}


# Edit post by Id
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    post_to_update = get_post_by_id(id)
    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found.")
    post = post.dict()
    for i in ["title", "content", "published"]:
        post_to_update[i] = post[i]
    return {"updated_post": post_to_update}


# Delete post by Id
@app.delete("/posts/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int):
    post = get_post_by_id(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found.")
    my_posts.remove(post)
    return {"deleted_post": post}
