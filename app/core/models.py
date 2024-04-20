from datetime import datetime
from typing import List
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, Integer, Text, String, func


"""
Database models
"""


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    todos: Mapped[List["Todo"]] = relationship(back_populates="owner", cascade="all, delete-orphan", single_parent=True)


class Todo(Base):
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=func.localtimestamp())
    
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    owner: Mapped["User"] = relationship(back_populates="todos")

    def __init__(self, title: str, owner_id: int, description: Text) -> None:
        """
        initialize a new Task with the provided title and owner Id.
        """
        self.title = title
        self.owner_id = owner_id
        self.description = description