from typing import Optional, List

from spotify_connectors.spotify_web_api_user import SpotifyWebAPIUser
from recommender_system.algorithm.nn_recommender import NearestNeighborsRecommender
from recommender_system.session.listening_session import MusicListeningSession
from common.data_transfer.models import SessionSettings


class MusicOs:

    def __init__(self):
        self.recommender = NearestNeighborsRecommender()
        self._spotify_web_api = SpotifyWebAPIUser()
        self._session = MusicListeningSession()


    def reset_session(self):
        self._session.clear_session()
    

    def add_playlist_to_session(self, playlist_id: str, user_id: str):
        tracks = self.recommender._data_provider.get_playlist_tracks(playlist_id)
        self._session.add_to_pool(tracks, user_id)
    
    
    def add_track_to_session(self, track_id: str, user_id: str):
        track = self.recommender._data_provider.get_track(track_id)
        self._session.add_to_pool([track], user_id)
    
    
    def get_track_pool_clusters(self):
        track_pool = self._session.get_track_pool()
        
        vectors = self.recommender.get_track_pool_vectors(
            [item.track for item in track_pool.values()]
        )
        
        if len(vectors) <= 0:
            return []
        
        tsne_with_cluster = self.recommender._profile_creator.get_tsne_points_with_cluster(list(vectors.values()))
        
        track_ids = list(vectors.keys())
        track_pool_clusters = []
        for tsne_point, track_id in zip(tsne_with_cluster, track_ids):
            track = self.recommender._data_provider.get_track(track_id)
            track_pool_clusters.append({
                'track_id': track_id,
                'track_name': f"{track.name_artists[0]} - {track.name}",
                'cluster': tsne_point[1],
                'tsne_coordinate': tsne_point[0]
            })
            
        return track_pool_clusters


    def generate_session_recommendations(
        self,
        output_playlist_id: str,
        settings: Optional[SessionSettings] = None,
        add_to_spotify_playlist: Optional[bool] = False
    ):
        recommendations = self.recommender.recommend_k_tracks_for_track_pool(
            track_pool=self._session.get_track_pool(),
            session_settings=settings
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
        settings: Optional[SessionSettings] = None,
        add_to_spotify_playlist: Optional[bool] = False
    ) -> Optional[List[str]]:

        recommendations = self.recommender.recommend_k_tracks_for_playlist(
            playlist_id=playlist_id,
            settings=settings
        )

        if add_to_spotify_playlist:

            self._spotify_web_api.replace_playlist_tracks(
                playlist_id=output_playlist_id,
                tracks_id=[recommendation.track.id for recommendation in recommendations]
            )

        return [(recommendation.track.name_artists[0], recommendation.track.name) for recommendation in recommendations]

    
    def get_session_stats(self):
        return self._session.get_session_statistics()
    

    def add_session_user(self, user_id: str) -> bool:
        return self._session.add_user(user_id)

    
    def get_session_users(self) -> List[str]:
        return self._session.get_users()
    

    def remove_session_user(self, user_id: str) -> bool:
        return self._session.remove_user(user_id)