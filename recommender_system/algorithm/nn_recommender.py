import numpy as np

from typing import List, Optional, Dict, Tuple
from numpy.typing import NDArray
from sklearn.neighbors import NearestNeighbors

from recommender_system.algorithm.profile_creator import ProfileCreator
from recommender_system.algorithm.curator import MusicCurator
from recommender_system.data_engineering.data_provider import DataProvider
from common.data_transfer.models import SessionSettings
from common.domain.models import (
    Track, 
    Artist, 
    RepresentationVector, 
    RecommendedTrack
)


class NearestNeighborsRecommender:

    def __init__(self):
        self._data_provider = DataProvider()
        self._profile_creator = ProfileCreator()
        self._recommender_model = NearestNeighbors(
            n_neighbors=60,
            metric='cosine'
        )
        self._curator = MusicCurator()
        self._fit_data_keys: List[str] = None
        self.prepare_recommender()


    def prepare_recommender(self):
        track_vectors = self._data_provider.get_all_representation_vectors()
        self._fit_data_keys = list(track_vectors.keys())
        self._fit_model(
            [np.nan_to_num(track_repr_vector, nan=-1) for track_repr_vector in track_vectors.values()]
        )


    def _fit_model(
        self,
        fit_data: List[NDArray]
    ):
        self._recommender_model.fit(fit_data)


    def find_k_most_similar_tracks(
        self,
        category: int,
        track_vector: RepresentationVector,
        exclude_tracks: Optional[List[Track]]
    ) -> List[RecommendedTrack]:
        """Find K most similar tracks based on representation vector

        Args:
            track_vectors (RepresentationVector): repr vector
            exclude_tracks (Optional[List[Track]]): tracks to be excluded

        Returns:
            List[RecommendedTrack]: neighbors found, with score and category
        """
        
        distances, neighbors = self._recommender_model.kneighbors(
            track_vector.reshape(1, -1), 
            return_distance=True
        )

        return [
            RecommendedTrack(
                track=self._data_provider.get_track(self._fit_data_keys[ngbr]),
                score=distance,
                category=category
            )   for distance, ngbr in zip(distances[0], neighbors[0])
        ]


    def get_track_pool_vectors(
        self,
        track_pool: List[Track]
    ) -> Dict[str, RepresentationVector]:
        
        track_pool_vectors = {}
        for track in track_pool:
            vector = self._data_provider.get_track_representation_vector(track)
            
            if vector is not None:
                track_pool_vectors[track.id] = vector
                
        return track_pool_vectors


    def create_settings_filter(
        self,
        session_settings: SessionSettings
    ):
        for sfilter in session_settings.__filters__:
            pass


    def recommend_k_tracks_based_on_track_pool(
        self,
        track_pool: List[Track],
        session_settings: SessionSettings
    ) -> List[RecommendedTrack]:
        """Recommend K tracks based on a pool of tracks

        Args:
            track_pool (List[Track]): track pool - set of track domain models

        Returns:
            List[Track]: recommendations
        """
        session_settings_filter = self.create_settings_filter(
            session_settings=session_settings
        )
        
        track_pool_vectors = self.get_track_pool_vectors(track_pool)
        
        if len(track_pool_vectors) <= 0:
            return []
        
        eigen_tracks, weights = self._profile_creator.create_profile_for_track_pool(
            tracks=list(track_pool_vectors.values())
        )
        
        tracks_to_recommend = []
        weight_per_category = {}
        for category, eigen_track in enumerate(eigen_tracks):
            # get recommendations
            similar_tracks: List[RecommendedTrack] = self.find_k_most_similar_tracks(
                category=category,
                track_vector=eigen_track,
                exclude_tracks=track_pool
            )
            tracks_to_recommend.extend(similar_tracks)
            weight_per_category[category] = weights[category]

        curated_recommendations = self._curator.curate_recommendation_list(
            track_pool=tracks_to_recommend,
            recommendation_number=30,
            weight_per_category=weight_per_category
        )

        return curated_recommendations


    def recommend_k_tracks_for_playlist(
        self,
        playlist_id: str,
        settings: SessionSettings
    ) -> List[RecommendedTrack]:

        tracks = self._data_provider.get_playlist_tracks(
            playlist_id=playlist_id
        )

        recommended_tracks = self.recommend_k_tracks_based_on_track_pool(
            track_pool=tracks,
            session_settings=settings
        )

        return recommended_tracks