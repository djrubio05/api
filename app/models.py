from datetime import datetime
from email.policy import default
from typing import Optional
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, LargeBinary, String, text
from sqlmodel import Relationship, SQLModel, Field

class User(SQLModel, table=True):
    __tablename__ = "users"

    email: str = Field(sa_column=Column(String, nullable=False, unique=True))
    password: bytes = Field(sa_column=Column(LargeBinary, nullable=False))
    id: int = Field(sa_column=Column(Integer, primary_key=True, nullable=False))
    created_at: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, 
                                                  server_default=text('now()')))

class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id: int = Field(sa_column=Column(Integer, primary_key=True, nullable=False))
    owner_id: int = Field(sa_column=Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False))
    title: str = Field(sa_column=Column(String, nullable=False))
    content: str = Field(sa_column=Column(String, nullable=False))
    published: bool = Field(sa_column=Column(Boolean, nullable=False, server_default="False"))
    created_at: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, 
                                                  server_default=text('now()')))
    
    owner: User = Relationship()

class Vote(SQLModel, table=True):
    __tablename__ = "votes"

    post_id: int = Field(sa_column=Column(Integer, ForeignKey("posts.id",ondelete="CASCADE"), primary_key=True, nullable=False))
    user_id: int = Field(sa_column=Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), primary_key=True, nullable=False))