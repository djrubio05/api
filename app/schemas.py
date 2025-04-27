from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, Field, conint

from app.models import User

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostOut(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

class PostVote(BaseModel):
    Post: PostOut
    votes: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    direction: Annotated[int, Field(strict=True, le=1, ge=0)]