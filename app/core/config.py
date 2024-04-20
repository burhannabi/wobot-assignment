import logging
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

log = logging.getLogger("uvicorn")

"""
Setup environment variables
"""

class OAuth2Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    TOKEN_EXPIRE_MINUTES: int


class Settings(OAuth2Settings, BaseSettings):
    ENVIRONMENT: str = "dev"
    DATABASE_URI: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")


@lru_cache()
def get_settings() -> Settings:
    log.info("Loading settings from environment")
    return Settings()