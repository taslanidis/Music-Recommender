from typing import Optional, List

from spotify_connectors.spotify_web_api_user import SpotifyWebAPIUser
from recommender_system.algorithm.nn_recommender import NearestNeighborsRecommender


class MusicOs:

    def __init__(self):
        self.recommender = NearestNeighborsRecommender()
        self._spotify_web_api = SpotifyWebAPIUser()

    
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