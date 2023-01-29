import numpy as np

from typing import Dict, List

from common.database.local_storage import LocalStorage
from common.domain.models import Track, Artist, RepresentationVector
from recommender_system.data_engineering.data_processing import DataProcessor
from spotify_connectors.spotify_web_api import SpotifyWebAPI


class DataProvider:

    _track_representation_vectors: Dict[str, RepresentationVector] = None
    _tracks: Dict[str, Track] = None
    _artists: Dict[str, Artist] = None
    
    def __init__(self):
        self._db = LocalStorage()
        self._spotify_web_api = SpotifyWebAPI()
        self._data_processor = DataProcessor()
        self._tracks = self._db.load_tracks()
        self._artists = self._db.load_artists()
            
        self._data_processor.fit_normalizer(self._tracks)
        
        self._track_representation_vectors = self._data_processor._initialize_track_representation_vectors(
            self._tracks.values()
        )
    

    def get_all_available_tracks(self):
        return self._tracks


    def get_all_available_artists(self):
        return self._artists


    def get_track(self, track_id: str) -> List[Track]:
        #TODO: hit spotify api to store it if not exists
        return self._tracks[track_id]
    

    def get_all_representation_vectors(self):
        return self._track_representation_vectors
    
    
    def get_playlist_tracks(self, playlist_id: str) -> List[Track]:
        enhanced_tracks = self._spotify_web_api.get_playlist_tracks_with_audio_features(
            playlist_id=playlist_id
        )
        
        # Create Track domain model from dto
        tracks = ...
        
        return tracks
    
    
    def get_track_representation_vector(
        self,
        track: Track
    ) -> RepresentationVector:
        #TODO: hit spotify api to store it if not exists
        if track.id in self._track_representation_vectors:
            return self._track_representation_vectors[track.id]
        
        return self._data_processor.create_track_representation_vector(track)
