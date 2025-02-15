from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Env(BaseSettings):
    openai_api_key: str

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_env() -> Env:
    """
    Create and cache an instance of the Env class.
    Using lru_cache to ensure we don't load the .env file multiple times.
    """
    return Env()


env = get_env()
