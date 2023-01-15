import numpy as np

from typing import List, Optional
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

from recommender_system.algorithm.profile_creator import ProfileCreator
from common.data_transfer.models import EnhancedTrack, TrackAudioFeatures
from common.database.mongo_db import MongoDatabase
from spotify_connectors.spotify_web_api import SpotifyWebAPI


# TODO: create various recommenders, such as EigenTrackRecommender, SimilarArtistRecommender etc.


class SimilarArtistsRecommender:

    def __init__(self):
        self._db = MongoDatabase()
        self._tracks = self._db.load_all_tracks()
        self._artists = self._db.load_all_artists()
        self._spotify_web_api = SpotifyWebAPI()
        self._profile_creator = ProfileCreator()
        self._profile_creator.prepare_profiler(
            fit_data=[track.audio_features for track in self._tracks]
        )
        self._model = NearestNeighbors(
            n_neighbors=20,
            metric='l2',
            algorithm='ball_tree'
        )
        self._normalizer = StandardScaler()
        self.prepare_recommender()


    def prepare_recommender(self):
        self._fit_normalizer([track.audio_features for track in self._tracks])
        self._fit_model([track.audio_features for track in self._tracks])

    
    def _fit_normalizer(
        self,
        fit_data: List[TrackAudioFeatures]
    ):
        self._normalizer.fit(
            [data_point.to_numpy() for data_point in fit_data]
        )


    def _fit_model(
        self,
        fit_data: List[TrackAudioFeatures]
    ):
        normalized_fit_data = self._normalizer.transform(
            [data_point.to_numpy() for data_point in fit_data]
        )

        self._model.fit(
            normalized_fit_data
        )


    def find_k_most_similar_tracks(
        self,
        audio_features: TrackAudioFeatures,
        exclude_tracks: Optional[List[EnhancedTrack]]
    ) -> List[EnhancedTrack]:
        """
        Find the K most similar tracks, to the one provided
        It can also be used with a constraint of a set of tracks to be avoided

        Returns: List[str] (All the spotify track ids)
        """
        features = audio_features.to_numpy().reshape(1,-1)
        features = self._normalizer.transform(
            features
        )
        
        neighbors = self._model.kneighbors(
            features, 
            return_distance=False
        )

        return [self._tracks[ngbr] for ngbr in neighbors[0]]


    def recommend_k_tracks_based_on_track_pool(
        self,
        track_pool: List[EnhancedTrack]
    ) -> List[EnhancedTrack]:
        """
        Recommend k tracks based on a track pool input

        Returns: List[str] (All the spotify track ids)
        """
        eigen_track = self._profile_creator.create_profile_for_track_pool(
            tracks=track_pool
        )

        tracks_to_recommend = self.find_k_most_similar_tracks(
            audio_features=eigen_track,
            exclude_tracks=track_pool
        )

        return tracks_to_recommend


    def recommend_k_tracks_for_playlist(
        self,
        playlist_id: str
    ) -> List[EnhancedTrack]:

        enhanced_tracks = self._spotify_web_api.get_playlist_tracks_with_audio_features(
            playlist_id=playlist_id
        )

        recommended_tracks = self.recommend_k_tracks_based_on_track_pool(
            track_pool=enhanced_tracks
        )

        return recommended_tracks