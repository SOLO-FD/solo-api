from functools import lru_cache
from pydantic_settings import BaseSettings
# from typing import Optional


class Settings(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///dev.db"


@lru_cache
def get_settings():
    return Settings()
