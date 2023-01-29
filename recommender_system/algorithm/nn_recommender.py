from typing import List, Optional
from numpy.typing import NDArray
from sklearn.neighbors import NearestNeighbors

from recommender_system.algorithm.profile_creator import ProfileCreator
from recommender_system.data_engineering.data_provider import DataProvider
from common.domain.models import Track, Artist, RepresentationVector


class NearestNeighborsRecommender:

    def __init__(self):
        self._data_provider = DataProvider()
        self._profile_creator = ProfileCreator()
        self._recommender_model = NearestNeighbors(
            n_neighbors=20,
            metric='cosine'
        )
        self._fit_data_keys: List[str] = None
        self.prepare_recommender()


    def prepare_recommender(self):
        track_vectors = self._data_provider.get_all_representation_vectors()
        self._fit_data_keys = list(track_vectors.keys())
        self._fit_model(
            [track_repr_vector for track_repr_vector in track_vectors.values()]
        )


    def _fit_model(
        self,
        fit_data: List[NDArray]
    ):
        self._recommender_model.fit(fit_data)


    def find_k_most_similar_tracks(
        self,
        track_vector: RepresentationVector,
        exclude_tracks: Optional[List[Track]]
    ) -> List[Track]:
        """Find K most similar tracks based on representation vector

        Args:
            track_vectors (RepresentationVector): repr vector
            exclude_tracks (Optional[List[Track]]): tracks to be excluded

        Returns:
            List[Track]: neighbors found
        """
        
        neighbors = self._recommender_model.kneighbors(
            track_vector, 
            return_distance=False
        )

        return [
            self._data_provider.get_track(self._fit_data_keys[ngbr]) for ngbr in neighbors[0]
        ]


    def recommend_k_tracks_based_on_track_pool(
        self,
        track_pool: List[Track]
    ) -> List[Track]:
        """Recommend K tracks based on a pool of tracks

        Args:
            track_pool (List[Track]): track pool - set of track domain models

        Returns:
            List[Track]: recommendations
        """
        track_pool_vectors = [
            self._data_provider.get_track_representation_vector(track) for track in track_pool
        ]
        eigen_tracks = self._profile_creator.create_profile_for_track_pool(
            tracks=track_pool_vectors
        )
        
        tracks_to_recommend = []
        for eigen_track in eigen_tracks:
            tracks_to_recommend += self.find_k_most_similar_tracks(
                track_vectors=eigen_track,
                exclude_tracks=track_pool
            )

        # TODO: check for duplicates
        return tracks_to_recommend


    def recommend_k_tracks_for_playlist(
        self,
        playlist_id: str
    ) -> List[Track]:

        tracks = self._data_provider.get_playlist_tracks(
            playlist_id=playlist_id
        )

        recommended_tracks = self.recommend_k_tracks_based_on_track_pool(
            track_pool=tracks
        )

        return recommended_tracks