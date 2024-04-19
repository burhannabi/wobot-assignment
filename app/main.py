from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends

from app.core.database import get_db
from app.core.models import Base
from .core.config import Settings, get_settings
from app.core.database import engine
import logging
from app.api.routers import crud


log = logging.getLogger("uvicorn")

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(engine)

        get_db()
        log.info("Loading database session. Please wait...")
        yield

    finally:
        log.info("Shutiing down...")
        engine.dispose()

def create_application() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(crud.router)

    return app

app = create_application()

@app.get("/ping")
def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong",
        "environment": settings.ENVIRONMENT
        } 