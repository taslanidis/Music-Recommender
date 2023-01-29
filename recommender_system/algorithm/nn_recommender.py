from typing import List, Optional
from numpy.typing import NDArray
from sklearn.neighbors import NearestNeighbors

from recommender_system.algorithm.profile_creator import ProfileCreator
from recommender_system.data_engineering.data_provider import DataProvider
from spotify_connectors.spotify_web_api import SpotifyWebAPI


class NearestNeighborsRecommender:

    def __init__(self):
        self._data_provider = DataProvider()
        self._spotify_web_api = SpotifyWebAPI()
        self._profile_creator = ProfileCreator()
        self._recommender_model = NearestNeighbors(
            n_neighbors=20,
            metric='cosine'
        )
        self.prepare_recommender()


    def prepare_recommender(self):
        self._fit_model(
            [track_repr_vector for track_repr_vector in self._data_provider.get_all_representation_vectors()]
        )


    def _fit_model(
        self,
        fit_data: List[NDArray]
    ):
        self._recommender_model.fit(fit_data)


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
        
        neighbors = self._recommender_model.kneighbors(
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
        eigen_tracks = self._profile_creator.create_profile_for_track_pool(
            tracks=track_pool
        )
        
        tracks_to_recommend = []
        for eigen_track in eigen_tracks:
            tracks_to_recommend += self.find_k_most_similar_tracks(
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