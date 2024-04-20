from datetime import datetime, timezone
import logging
import pytz
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.models import User

uvicorn_logger = logging.getLogger("uvicorn")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#supress the passlib version warning
logging.getLogger('passlib').setLevel(logging.ERROR)

#create hash of passwrod
def hash(password: str):
    return pwd_context.hash(password)

#verify hash of password
def verify(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


#custom exceptions
class TaskNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Task/s not found")

class InvalidCredentials(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail="Invalid credentials. Please try again!", headers={"WWW-Authenticate": "Bearer"})

class InternalServerError(HTTPException):
    def __init__(self, e):
        super().__init__(status_code=500, detail=str(e))

#get local time
def get_ist():
    utc_now = datetime.now(timezone.utc)
    local_timezone = pytz.timezone("Asia/Kolkata")
    local_time = utc_now.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    return local_time

#get current user
def get_user(sub: str, db: Session):
    user = db.query(User).filter_by(username=sub).first()
    if not user:
        raise InvalidCredentials()
    return user