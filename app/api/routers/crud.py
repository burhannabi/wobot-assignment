from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from ..schemas.posts import PostIn, PostOut, Detail
from app.core.models import Post
from sqlalchemy.exc import SQLAlchemyError

from app.misc.helpers import InternalServerError, PostNotFound

router = APIRouter(prefix="/post", tags=['Posts'])


@router.post("/create", status_code=201, response_model=Detail)
async def create_post(payload: PostIn, db: Session = Depends(get_db)):
    """
    Endpoint to add a post
    """
    try:

        new_post = Post(**payload.model_dump())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return {"detail": "Post added successfully!"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

@router.get("/fetch", status_code=200, response_model=List[PostOut])
async def fetch_all_posts(db: Session = Depends(get_db)):
    """
    Endpoint to fetch all posts
    """

    try:
        all_posts = db.query(Post).all()
        if not all_posts:
            raise PostNotFound()
        
        return all_posts
    
    except SQLAlchemyError as e:
        db.rollback()
        raise InternalServerError(e)
    

@router.get("/{id}", status_code=200, response_model=PostOut)
async def fetch_single_post(id: int, db: Session = Depends(get_db)):
    """
    Endpoint to fetch a single post
    """
    try:
        post = db.query(Post).filter_by(id=id).first()
        if not post:
            raise PostNotFound()
        
        return post
    
    except SQLAlchemyError as e:
        db.rollback()
        raise InternalServerError(e)
    

@router.put("/{id}", status_code=201, response_model=PostOut)
async def update_post(id: int, payload: PostIn, db: Session = Depends(get_db)):
    """
    Endpoint to update a post
    """

    try:
        # fetch existing post to update
        existing_post = db.query(Post).filter_by(id=id).first()
        
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(existing_post, field, value)

        db.commit()
        db.refresh(existing_post)
        return existing_post

    except SQLAlchemyError as e:
        db.rollback()
        raise InternalServerError(e)