from app.routers import user
from .. import models, schemas, oauth2
from ..database import SessionDep
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlmodel import col, or_, select
from sqlalchemy import func
from typing import Annotated, List, Optional


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostVote])
# @router.get("/")
def get_posts(session: SessionDep,
              current_user: Annotated[int, Depends(oauth2.get_current_user)],
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cur.execute("""SELECT * FROM posts """)
    # posts = cur.fetchall()
    search_parameter = or_(col(models.Post.title).contains(search),col(models.Post.content).contains(search))
    join_query = select(models.Post, func.count(models.Vote.post_id).label(name='votes')).join(models.Vote, models.Post.id == models.Vote.post_id, isouter = True).group_by(models.Post.id)
    query = join_query.limit(limit).offset(skip).filter(search_parameter)

    posts = session.exec(query).all()

    posts =  list(map(lambda x:x._mapping,posts))   #add votes column name to result posts

    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_posts(post: schemas.PostCreate, session: SessionDep, 
                 current_user: Annotated[int, Depends(oauth2.get_current_user)]):
    # cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                # (post.title, post.content, post.published))
    # new_post = cur.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    
    return new_post

@router.get("/{id}", response_model=schemas.PostVote)
def get_post(id: int, session: SessionDep,
             current_user: Annotated[int, Depends(oauth2.get_current_user)]):
    # cur.execute("""SELECT * from posts WHERE id = %s """, (id,))
    # post = cur.fetchone()
    # post = session.get(models.Post, id)
    join_query = select(models.Post, func.count(models.Vote.post_id).label(name='votes')).join(models.Vote, models.Post.id == models.Vote.post_id, isouter = True).group_by(models.Post.id)
    query = join_query.filter(models.Post.id == id)
    post = session.exec(query).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, session: SessionDep,
                current_user: Annotated[int, Depends(oauth2.get_current_user)]):
    # cur.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(id,))
    # deleted_post = cur.fetchone()
    # conn.commit()
    post = session.exec(select(models.Post).filter(models.Post.id == id)).first()

    if post == None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                       detail = f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                                             detail = f"Not authorized to perform requested action")
    
    session.delete(post)
    session.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostOut)
def update_post(id: int, post: schemas.PostCreate, session: SessionDep,
                current_user: Annotated[int, Depends(oauth2.get_current_user)]):
    # cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
                # (post.title, post.content, post.published, id))
    # updated_post  = cur.fetchone()
    # conn.commit()
    fetched_post = session.exec(select(models.Post).filter(models.Post.id == id)).first()
    
    if fetched_post == None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                       detail = f"post with id: {id} does not exist")
    
    if fetched_post.owner_id != current_user.id: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                                             detail = f"Not authorized to perform requested action")
    
    post_dict = post.model_dump()

    for field, value in post_dict.items():
        setattr(fetched_post, field, value)

    session.add(fetched_post)
    session.commit()
    session.refresh(fetched_post)

    return fetched_post