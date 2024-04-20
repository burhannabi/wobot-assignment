from pydantic import BaseModel
from typing import Text
from datetime import datetime


"""
Pydantic schemas for data validation and serialization
"""

class Detail(BaseModel):
    detail: str

class TaskIn(BaseModel):
    title: str
    description: Text

class TaskOut(TaskIn):
    id: int
    created_at: datetime
    completed: bool

class TaskUpdate(TaskIn):
    completed: bool