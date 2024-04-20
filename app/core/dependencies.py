from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from ..core.database import get_db
from ..misc.helpers import InvalidCredentials, get_user
from ..api.schemas.auth import TokenData
from .config import get_settings, Settings


settings: Settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# access token for jwt athentication
async def create_access_token(data: TokenData):

    to_encode = {
        "sub": data.sub,
        "exp": data.exp,
        "iat": data.iat
    }

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt

    
# verify and get authenticated user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, [settings.ALGORITHM])
        sub: str = payload["sub"]
        if not sub:
            raise InvalidCredentials()
        
    except JWTError:
        raise InvalidCredentials()
    
    user = get_user(sub, db)

    if user is None:
        raise InvalidCredentials()
    
    return user