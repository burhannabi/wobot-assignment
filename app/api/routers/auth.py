from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from ..schemas.task import Detail
from ..schemas.auth import Token, TokenData, UserIn
from ...core.config import Settings, get_settings
from ...core.dependencies import get_db, create_access_token
from ...core.models import User
from ...misc.helpers import InternalServerError, get_ist, verify, hash, InvalidCredentials


settings: Settings = get_settings()


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", status_code=200, operation_id="login", response_model=Token)
async def login(payload: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Token:

    """
    Login to get authenticated.
    """
    try:
        exiisting_user = db.query(User).filter_by(username=payload.username).first()
        if not exiisting_user:
            raise InvalidCredentials()
        if not verify(payload.password, exiisting_user.password):
            raise InvalidCredentials()
        
        localtime = get_ist()
        exp = localtime + timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
        iat = localtime
        token_data = TokenData(sub=payload.username, exp=exp, iat=iat)

        access_token = await create_access_token(token_data)

        return {"access_token": access_token, "token_type": "Bearer"}

    except SQLAlchemyError as e:
        db.rollback()
        raise InternalServerError(e)

@router.post("/register", status_code=status.HTTP_201_CREATED, operation_id="register", response_model=Detail)
async def create_user(payload: UserIn, db: Session = Depends(get_db)):
    """
    Register to the system.
    """
    
    try:
        existing_user = db.query(User).filter_by(username=payload.username).first()

        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with the username '{payload.username}' already exists!")
        
        hashed_password = hash(payload.password)
        payload.password = hashed_password
        new_user = User(**payload.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"detail": f"User with username '{payload.username}' created!"}
    
    except SQLAlchemyError as e:
        db.rollback()
        raise InternalServerError(e)
