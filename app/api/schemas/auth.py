from datetime import datetime
from pydantic import BaseModel

"""
Pydantic schemas for data validation and serialization
"""

class TokenData(BaseModel):
    sub: str
    iat: datetime 
    exp: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class UserIn(BaseModel):
    username: str
    password: str