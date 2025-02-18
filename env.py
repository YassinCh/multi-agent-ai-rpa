from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from pydantic import Field, StrictStr
from dotenv import load_dotenv


class Env(BaseSettings):
    OPENAI_API_KEY: str
    LANGSMITH_API_KEY: str

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_env() -> Env:
    load_dotenv()
    """
    Create and cache an instance of the Env class.
    Using lru_cache to ensure we don't load the .env file multiple times.
    """
    return Env()


env = get_env()
