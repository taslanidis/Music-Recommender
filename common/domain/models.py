import numpy as np

from numpy.typing import NDArray
from typing import Dict, List
from datetime import datetime

# These are the models that will be used internally by our models

class Track:
    id: str = None
    release_date: datetime = None
    track_age: float = None
    popularity: float = None
    danceability: float = None
    tempo: float = None
    valence: float = None
    energy: float = None
    loudness: float = None
    speechiness: float = None
    instrumentalness: float = None
    liveness: float = None
    artist_mean_popularity: float = None
    artist_max_popularity: float = None
    genres: List[str] = None
    id_artists: List[str] = None
    

    scaled_features = [
        'track_age',
        'tempo',
        'popularity',
        'valence',
        'energy',
        'loudness',
        'danceability',
        'speechiness',
        'acousticness',
        'instrumentalness',
        'liveness',
        'artist_mean_popularity'
    ]
    
    
    def to_numpy_normalizable_part(self) -> NDArray:
       return np.array([getattr(self, key) for key in self.scaled_features])


class Artist:
    id: str
    followers: int
    genres: List[str] = None
    name: str
    popularity: float


class RepresentationVector(np.ndarray):
    pass