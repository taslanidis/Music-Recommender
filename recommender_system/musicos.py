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
        self._session.add(tracks)


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
                tracks_id=[track.id for track in recommendations]
            )

        return [(track.artists[0].name, track.name) for track in recommendations]


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
                tracks_id=[track.id for track in recommendations]
            )

        return [(track.artists[0].name, track.name) for track in recommendations]

    
    def get_session_stats(self):
        return self._session.get_session_statistics()