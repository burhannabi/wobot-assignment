import logging
import os
from functools import lru_cache

from pydantic import BaseModel, AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

log = logging.getLogger("uvicorn")


class OAuth2Settings(BaseModel):
    SECRET_KEY: str
    ALGORITHM: str
    TOKEN_EXPIRE_MINUTES: int


class Settings(BaseSettings):
    ENVIRONMENT: str = "dev"
    DATABASE_URI: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")


@lru_cache()
def get_settings() -> Settings:
    log.info("Loading settings from environment")
    return Settings()