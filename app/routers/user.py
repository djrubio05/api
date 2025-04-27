from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from .. import models, schemas, utils
from ..database import SessionDep
from sqlmodel import select

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, session: SessionDep):

    #hash the password - user.password
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, session: SessionDep):
    user = session.exec(select(models.User).filter(models.User.id == id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    
    return user