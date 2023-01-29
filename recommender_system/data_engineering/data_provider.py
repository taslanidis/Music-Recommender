import numpy as np

from typing import Dict, List

from common.database.local_storage import LocalStorage
from common.domain.models import Track, Artist, RepresentationVector
from recommender_system.data_engineering.data_processing import DataProcessor


class DataProvider:

    _track_representation_vectors: List[RepresentationVector] = None
    _tracks: Dict[str, Track] = None
    _artists: Dict[str, Artist] = None
    
    def __init__(self):
        self._db = LocalStorage()
        self._data_processor = DataProcessor()
        self._tracks = self._db.load_tracks()
        self._artists = self._db.load_artists()
            
        self._data_processor.fit_normalizer(self._tracks)
        
        self._track_representation_vectors = self._data_processor._create_track_representation_vectors(
            self._tracks
        )
    

    def get_all_available_tracks(self):
        return self._tracks


    def get_all_available_artists(self):
        return self._artists


    def get_all_representation_vectors(self):
        return self._track_representation_vectors
