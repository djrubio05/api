from fastapi import FastAPI
from sqlmodel import SQLModel
from .database import engine
from .routers import post, user, auth, votes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["https://www.google.com",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def root():
    return {"message": "Welcome to my API, my guy"}
