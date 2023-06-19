import numpy as np

from typing import Dict, List, Optional

from common.database.local_storage import LocalStorage
from common.domain.models import Track, Artist, RepresentationVector, ArtistSearchableObject
from common.converters.interfaces import TrackConversionInterface, ArtistConversionInterface
from recommender_system.data_engineering.data_processing import DataProcessor
from spotify_connectors.spotify_web_api import SpotifyWebAPI
from common import utils


class DataProvider:

    _track_representation_vectors: Dict[str, RepresentationVector] = None
    _tracks: Dict[str, Track] = None
    _artists: Dict[str, Artist] = None
    
    def __init__(
        self, 
        create_hash_map_for_artists: Optional[bool] = False,
        use_as_mapper_only: Optional[bool] = False
    ):
        self._db = LocalStorage()
        self._spotify_web_api = SpotifyWebAPI()
        self._data_processor = DataProcessor()
        self._tracks = self._db.get_tracks()
        self._artists = self._db.get_artists()
        
        if not use_as_mapper_only:
            
            self._data_processor.fit_normalizer(self._tracks.values())
            
            self._track_representation_vectors = self._data_processor._initialize_track_representation_vectors(
                self._tracks.values()
            )
        
        if create_hash_map_for_artists:
            self._artist_hash_map: Dict[str, List[ArtistSearchableObject]] = {}
            
            for artist in self._artists.values():
                artist_name_clean = utils.clear_name_text(artist.name)
                
                if artist_name_clean[0] not in self._artist_hash_map:
                    self._artist_hash_map[artist_name_clean[0]] = []
                
                self._artist_hash_map[artist_name_clean[0]].append(
                    ArtistSearchableObject(
                        name = utils.clear_name_text(artist_name_clean),
                        id = artist.id
                    )
                )
                
            # sort hash bins
            for key in self._artist_hash_map.keys():
                self._artist_hash_map[key] = sorted(self._artist_hash_map[key], key = lambda x: x.name, reverse=False)
    

    def get_all_available_tracks(self):
        return self._tracks


    def get_all_available_artists(self):
        return self._artists


    def get_track(self, track_id: str) -> Track:
        if track_id not in self._tracks:

            enhanced_track = self._spotify_web_api.get_enhanced_track(track_id)

            self._tracks[track_id] = TrackConversionInterface.convert_dto_to_domain(
                enhanced_track
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
    
    
    def artist_mapper(
        self,
        artist_name: str
    ) -> Artist:
        
        artist_name_clean = utils.clear_name_text(artist_name)
        
        artists_bin = self._artist_hash_map.get(artist_name_clean[0], [])
        
        for artists in artists_bin:
            if artist_name_clean == artists.name:
                return self._artists[artists.id]
