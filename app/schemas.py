from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Base class for Posts
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


#  Okay, now we're talking. This class is based on PostBase and has other extended types
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
