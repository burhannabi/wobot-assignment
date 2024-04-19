from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import TIMESTAMP, Text, String, func


class Base(DeclarativeBase):
    pass


class Post(Base):
    
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    content: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=func.localtimestamp())