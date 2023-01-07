from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    scope: str = 'user-library-read'
    CLIENT_ID: str
    CLIENT_SECRET: str
    spotify_redirect_uri: str = "http://localhost:8025"
    limit_max: int = 50
    backoff_factor: int = 90

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
