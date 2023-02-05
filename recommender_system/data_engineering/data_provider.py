import numpy as np

from typing import Dict, List, Optional

from common.database.local_storage import LocalStorage
from common.domain.models import Track, Artist, RepresentationVector
from common.converters.interfaces import TrackConversionInterface, ArtistConversionInterface
from recommender_system.data_engineering.data_processing import DataProcessor
from spotify_connectors.spotify_web_api import SpotifyWebAPI


class DataProvider:

    _track_representation_vectors: Dict[str, RepresentationVector] = None
    _tracks: Dict[str, Track] = None
    _artists: Dict[str, Artist] = None
    
    def __init__(self):
        self._db = LocalStorage()
        self._spotify_web_api = SpotifyWebAPI()
        self._data_processor = DataProcessor(track_features_weight=2)
        self._tracks = self._db.get_tracks()
        self._artists = self._db.get_artists()
            
        self._data_processor.fit_normalizer(self._tracks.values())
        
        self._track_representation_vectors = self._data_processor._initialize_track_representation_vectors(
            self._tracks.values()
        )
    

    def get_all_available_tracks(self):
        return self._tracks


    def get_all_available_artists(self):
        return self._artists


    def get_track(self, track_id: str) -> Track:
        if track_id not in self._tracks:
            # TODO: needs thought (get genres in converters)
            self._tracks[track_id] = TrackConversionInterface.convert_dto_to_domain(
                self._spotify_web_api.get_track(track_id)
            )
        return self._tracks[track_id]
    
    
    def get_artist(self, artist_id: str) -> Artist:
        if artist_id not in self._artists:
            self._artists[artist_id] = ArtistConversionInterface.convert_dto_to_domain(
                self._spotify_web_api.get_artists([artist_id])[0]
            )
        return self._artists[artist_id]


    def get_all_representation_vectors(self):
        return self._track_representation_vectors
    
    
    def get_playlist_tracks(self, playlist_id: str) -> List[Track]:
        enhanced_tracks = self._spotify_web_api.get_playlist_tracks_with_audio_features(
            playlist_id=playlist_id
        )

        # Append extra information for artists - needed for domain models
        # If artists does not exist in our DB, hit spotify API
        for track in enhanced_tracks:
            artist_domain_models = []
            for artist in track.artists:
                artist_domain_models.append(
                    self.get_artist(artist.id)
                )
            track.artists = artist_domain_models

        # Create Track domain model from dto
        tracks = [TrackConversionInterface.convert_dto_to_domain(track) for track in enhanced_tracks]
        
        # append tracks in local db
        for track in tracks:
            if track.id not in self._tracks:
                self._tracks[track.id] = track

        return tracks
    
    
    def get_track_representation_vector(
        self,
        track: Track
    ) -> Optional[RepresentationVector]:

        if track.id in self._track_representation_vectors:
            return self._track_representation_vectors[track.id]
        
        self._track_representation_vectors[track.id] = self._data_processor.create_track_representation_vector(track)
        
        return self._track_representation_vectors[track.id]
    
    
    def get_artist_by_name(
        self,
        artist_name: str
    ) -> Artist:
        for artist_id in self._artists:
            # TODO: create more smart mappers
            if self._artists[artist_id].name == artist_name:
                return self._artists[artist_id]
