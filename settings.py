from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    scope: str = 'user-library-read'
    CLIENT_ID: str
    CLIENT_SECRET: str
    spotify_redirect_uri: str = "http://localhost:8025"
    limit_max: int = 50
    backoff_factor: int = 90
    
    artist_embeddings: str
    genre_embeddings: str
    genre_embeddings_size: int = 16
    artist_embeddings_size: int = 16
    
    track_local_stored_path: str = None
    artist_local_stored_path: str = None
    genre_vocab_local_stored_path: str = None
    track_representation_vectors_stored_path: str = None

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
