import spotipy
import logging
from typing import List
from spotipy.oauth2 import SpotifyOAuth

from settings import Settings, get_settings


class SpotifyWebAPIUser:
    
    scope = "playlist-modify-public"

    def __init__(self):
        self.settings: Settings = get_settings()
        self._CLIENT_ID = self.settings.CLIENT_ID
        self._CLIENT_SECRET = self.settings.CLIENT_SECRET
        self._sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope=self.scope, 
                client_id=self._CLIENT_ID, 
                client_secret=self._CLIENT_SECRET,
                redirect_uri=self.settings.spotify_redirect_uri
            )
        )
        self._logger = logging.getLogger('SpotifyWebAPIUser')

    
    def replace_playlist_tracks(
        self,
        playlist_id: str,
        tracks_id: List[str]
    ):
        self._sp.user_playlist_replace_tracks(
            user=self._sp.current_user()['id'],
            playlist_id=playlist_id,
            tracks=tracks_id
        )