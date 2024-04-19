
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import Settings, get_settings

settings: Settings = get_settings()

#create database connection
engine = create_engine(settings.DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()