from fastapi import HTTPException, status, Response, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas 

router = APIRouter()


# Get posts
@router.get("/posts", status_code=status.HTTP_200_OK, response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# Create posts
@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Get post by Id
@router.get("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def get_post_id(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found.")
    return post


# Edit post by Id
@router.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id: int, user_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found.")
    post.update(user_post.dict(), synchronize_session=False)
    db.commit()
    return post.first()


# Delete post by Id
@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found.")
    post.delete(synchronize_session=False)
    db.commit()
    return