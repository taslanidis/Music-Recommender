import numpy as np

from typing import List
from collections import Counter

from common.domain.models import Track

class MusicListeningSession:

    # keeping duplicates as weights
    _track_pool: List[Track]

    def __init__(self):
        self._track_pool = []

    
    def clear_session(self):
        self._track_pool = []


    def get_track_pool(self) -> List[Track]:
        return self._track_pool

    
    def add_to_pool(self, tracks: List[Track]):
        self._track_pool.extend(tracks)

    
    def calculate_genre_frequency(self):
        top_genres = {}
        for track in self._track_pool:
            for genre in track.genres:
                if genre not in top_genres:
                    top_genres[genre] = 0
                top_genres[genre] += 1
        return dict(Counter(top_genres).most_common(5))
    
    
    def get_session_statistics(self):
        return {
            'danceability_mean': np.mean([track.danceability for track in self._track_pool]),
            'energy_mean': np.mean([track.energy for track in self._track_pool]),
            'valence_mean': np.mean([track.valence for track in self._track_pool]),
            'instrumentalness_mean': np.mean([track.instrumentalness for track in self._track_pool]),
            'tempo_mean': np.mean([track.tempo for track in self._track_pool]),
            'track_number': len(self._track_pool),
            'top_genres': self.calculate_genre_frequency()
        }