from typing import Dict


# These are the models that will be used internally by our models

class Track:
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
    
    
    def get_normalizable_part(self) -> Dict:
        return {
            key: getattr(self, key) for key in self._attrs_to_normalize
        }



class Artist:
    pass