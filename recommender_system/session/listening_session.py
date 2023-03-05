import numpy as np

from typing import List, Dict
from collections import Counter

from common.domain.models import Track, TrackPoolItem
from recommender_system.algorithm.track_pool_processor import TrackPoolProcessor


class MusicListeningSession:

    _tracks_per_user: Dict[str, List[Track]]
    
    def __init__(self):
        self._tracks_per_user = {}

    
    def clear_session(self):
        self._tracks_per_user = {}


    def get_tracks_per_user(self) -> List[Track]:
        return self._tracks_per_user


    def get_track_pool(self) -> Dict[str, TrackPoolItem]:
        
        track_pool = TrackPoolProcessor.create_track_pool_from_dict(
            track_dict=self.get_tracks_per_user()
        )
        
        return track_pool

    
    def add_to_pool(self, tracks: List[Track], user_id: str):
        if user_id not in self._tracks_per_user:
            self._tracks_per_user[user_id] = []
        
        self._tracks_per_user[user_id].extend(tracks)
        
    
    def calculate_genre_frequency(self):
        top_genres = {}
        for item in self.get_track_pool().values():
            for genre in item.track.genres:
                if genre not in top_genres:
                    top_genres[genre] = 0
                top_genres[genre] += 1
        return dict(Counter(top_genres).most_common(10))
    
    
    def get_session_statistics(self):
        track_pool = self.get_track_pool()
        
        if len(track_pool) <= 0:
            return {}

        return {
            'danceability_mean': np.mean([item.track.danceability for item in track_pool.values()]),
            'energy_mean': np.mean([item.track.energy for item in track_pool.values()]),
            'valence_mean': np.mean([item.track.valence for item in track_pool.values()]),
            'instrumentalness_mean': np.mean([item.track.instrumentalness for item in track_pool.values()]),
            'tempo_mean': np.mean([item.track.tempo for item in track_pool.values()]),
            'tracks_number': len(track_pool),
            'top_genres': self.calculate_genre_frequency()
        }
