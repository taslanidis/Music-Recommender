from typing import Optional, List

from spotify_connectors.spotify_web_api_user import SpotifyWebAPIUser
from recommender_system.algorithm.nn_recommender import NearestNeighborsRecommender
from recommender_system.session.listening_session import MusicListeningSession


class MusicOs:

    def __init__(self):
        self.recommender = NearestNeighborsRecommender()
        self._spotify_web_api = SpotifyWebAPIUser()
        self._session = MusicListeningSession()


    def reset_session(self):
        self._session.clear_session()
    

    def add_playlist_to_session(self, playlist_id: str):
        tracks = self.recommender._data_provider.get_playlist_tracks(playlist_id)
        self._session.add_to_pool(tracks)
        
    
    def get_track_pool_clusters(self):
        tracks = self._session.get_track_pool()
        vectors = self.recommender.get_track_pool_vectors(tracks)
        tsne_with_cluster = self.recommender._profile_creator.get_tsne_points_with_cluster(vectors)
        
        track_ids = list(vectors.keys())
        track_pool_clusters = []
        for tsne_point, track_id in zip(tsne_with_cluster, track_ids):
            track_pool_clusters.append({
                'track_id': track_id,
                'cluster': tsne_point[1],
                'tsne_coordinate': tsne_point[0]
            })
            
        return track_pool_clusters


    def generate_session_recommendations(
        self,
        output_playlist_id: str,
        add_to_spotify_playlist: Optional[bool] = False
    ):
        recommendations = self.recommender.recommend_k_tracks_based_on_track_pool(
            track_pool=self._session.get_track_pool()
        )

        if add_to_spotify_playlist:

            self._spotify_web_api.replace_playlist_tracks(
                playlist_id=output_playlist_id,
                tracks_id=[recommendation.track.id for recommendation in recommendations]
            )

        return [(recommendation.track.name_artists[0], recommendation.track.name) for recommendation in recommendations]


    def recommend_k_tracks_for_playlist(
        self,
        playlist_id: str,
        output_playlist_id: str,
        add_to_spotify_playlist: Optional[bool] = False
    ) -> Optional[List[str]]:

        recommendations = self.recommender.recommend_k_tracks_for_playlist(
            playlist_id=playlist_id
        )

        if add_to_spotify_playlist:

            self._spotify_web_api.replace_playlist_tracks(
                playlist_id=output_playlist_id,
                tracks_id=[recommendation.track.id for recommendation in recommendations]
            )

        return [(recommendation.track.name_artists[0], recommendation.track.name) for recommendation in recommendations]

    
    def get_session_stats(self):
        return self._session.get_session_statistics()