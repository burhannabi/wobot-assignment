from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import HTTPException


class PostNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Post/s not found")

class InvalidCredentials(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail="Invalid credentials. Please try again!", headers={"WWW-Authenticate": "Bearer"})

class InternalServerError(HTTPException):
    def __init__(self, e):
        super().__init__(status_code=500, detail=str(e)) 