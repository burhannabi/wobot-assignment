from pydantic import BaseModel
from datetime import datetime


class Detail(BaseModel):
    detail: str

class PostIn(BaseModel):
    title: str
    content: str

class PostOut(PostIn):
    id: int
    created_at: datetime