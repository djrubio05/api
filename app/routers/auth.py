from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlmodel import select
from .. import models, database, schemas, utils, oauth2

router = APIRouter(
    tags=['Auth']
)

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()], session: database.SessionDep):
    
    fetched_user = session.exec(select(models.User).filter(models.User.email == user_credentials.username)).first()
    if not fetched_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    
    user_verified = utils.verify_password(user_credentials.password,fetched_user.password)
    if not user_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data = {"user_id": fetched_user.id})

    return {'access_token': access_token, "token_type" : "bearer"}