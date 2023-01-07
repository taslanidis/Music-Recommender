import spotipy
import logging
import requests
import urllib3

from spotipy.oauth2 import SpotifyClientCredentials
from typing import Optional, List

from common.data_transfer.models import (
    Artist, 
    Category, 
    EnhancedTrack, 
    Playlist, 
    Track, 
    TrackAudioFeaturesWithId
)
from settings import Settings, get_settings


class SpotifyWebAPI:

    def __init__(self, throughput_limiter: Optional[bool] = False):
        self.settings: Settings = get_settings()
        self._scope = self.settings.scope
        self._CLIENT_ID = self.settings.CLIENT_ID
        self._CLIENT_SECRET = self.settings.CLIENT_SECRET
        self._client_credentials_manager = SpotifyClientCredentials(
            client_id=self._CLIENT_ID, 
            client_secret=self._CLIENT_SECRET
        )
        self._sp = spotipy.Spotify(
            client_credentials_manager=self._client_credentials_manager,
            requests_session=self._create_custom_session(),
            requests_timeout=15
        )
        self.limit_max = self.settings.limit_max
        self._throughput_limiter = throughput_limiter
        self._logger = logging.getLogger('SpotifyWebAPI')


    def _create_custom_session(self):
        session = requests.Session()

        retry = urllib3.Retry(
            total=2,
            backoff_factor=self.settings.backoff_factor,
            status_forcelist=(429, 500, 502, 503, 504)
        )

        adapter = requests.adapters.HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        return session

    def get_audio_features_for_tracks(self, tracks: List[str]) -> List[TrackAudioFeaturesWithId]:
        
        if type(tracks) == str:
            return [TrackAudioFeaturesWithId(**self._sp.audio_features(tracks)[0])]

        audio_features = []
        max_tracks = 100

        for k in range(len(tracks) // max_tracks + 1):
            audio_features.extend(
                [TrackAudioFeaturesWithId(**track_audio_features) for track_audio_features in self._sp.audio_features(tracks[k:k+max_tracks])]
            )
        
        return audio_features


    def get_genres(self):
        return self._sp.recommendation_genre_seeds()


    def __fetch_parse_categories(
        self, 
        country: Optional[str] = None, 
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Category]:

        try:

            response = self._sp.categories(country = country, limit = limit, offset = offset)
            categories_unparsed = response.get('categories', {}).get('items', []) if response is not None else []
            
            categories = [Category(**item) for item in categories_unparsed]
            
            return categories

        except Exception as e:

            self._logger.error(f"Exception while fetching/parsing categories. Details: {e}")


    def get_categories(
        self, 
        country: str = None, 
        page_size: Optional[int] = 50, 
        limit: Optional[int] = None, 
        offset: Optional[int] = 0
    ) -> List[Category]:

        if limit and limit > self.limit_max:
            raise ValueError(f"Limit can not be larger than {self.limit_max}")
        
        if limit:
            return self.__fetch_parse_categories(country = country, limit = limit)
        
        categories: List[Category] = []
        counter: int = 0

        while True:
            categories_page = self.__fetch_parse_categories(
                country = country, 
                limit = page_size, 
                offset = offset + counter
            )
            
            if categories_page is None or len(categories_page) == 0:
                break

            categories.extend(categories_page)
            counter += page_size
        
        return categories


    def __fetch_parse_playlists(
        self, 
        category_id: int, 
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Playlist]:

        try:

            response = self._sp.category_playlists(
                category_id = category_id, 
                limit = limit, 
                offset = offset
            )
            categories_unparsed = response.get('playlists', {}).get('items', []) if response is not None else []
            
            categories = [Playlist(**item) for item in categories_unparsed]
            
            return categories

        except Exception as e:

            self._logger.error(f"Exception while fetching/parsing playlists. Details: {e}")


    def get_playlists_for_category(
        self, 
        category_id: int, 
        page_size: Optional[int] = 50, 
        limit: Optional[int] = None, 
        offset: Optional[int] = 0
    ) -> List[Playlist]:

        if limit and limit > self.limit_max:
            raise ValueError(f"Limit can not be larger than {self.limit_max}")
        
        if limit:
            return self.__fetch_parse_playlists(
                category_id = category_id, 
                limit = limit
            )
        
        playlists: List[Playlist] = []
        counter: int = 0

        while True:
            
            playlists_page = self.__fetch_parse_playlists(
                category_id = category_id, 
                limit = page_size, 
                offset = offset + counter
            )
            
            if playlists_page is None or len(playlists_page) == 0:
                break
            
            playlists.extend(playlists_page)
            counter += page_size
        
        return playlists


    def get_playlist_by_id(self, playlist_id: str) -> Optional[Playlist]:
        response = self._sp.playlist(playlist_id = playlist_id)
        return Playlist(**response) if response is not None else None


    def get_playlist_tracks(self, playlist_id: str) -> List[Track]:
        response = self._sp.playlist_tracks(playlist_id = playlist_id)
        try:
            return [
                Track(**item['track']) for item in response.get('items', [])
            ] if response is not None else []
        
        except Exception as e:
            self._logger.warning(f"Issue while trying to load tracks for playlist ID: {playlist_id}. Details: {e}")

        return []


    def get_playlist_tracks_with_audio_features(self, playlist_id: str) -> List[EnhancedTrack]:
        tracks = self.get_playlist_tracks(playlist_id = playlist_id)

        audio_features = self.get_audio_features_for_tracks(
            tracks=[track.id for track in tracks]
        )

        audio_features = {
            track_audio_features.id: track_audio_features for track_audio_features in audio_features
        }

        enhanced_tracks: List[EnhancedTrack] = []

        for track in tracks:

            enhanced_tracks.append(
                EnhancedTrack(audio_features=audio_features[track.id].dict(), **track.dict())
            )

        return enhanced_tracks


    def get_artists(
        self, 
        artist_ids: List[str]
    ) -> List[Artist]:

        artists: List = []
        counter: int = 0
        limit: int = 50
        
        while counter < len(artist_ids):

            artists += self._sp.artists(artists=artist_ids[counter:counter+limit]).get('artists', [])
            
            counter += limit
        
        return [Artist(**artist) for artist in artists]

    
    def enhance_tracks_with_artist_information(
        self, 
        tracks: List[EnhancedTrack]
    ) -> List[EnhancedTrack]:

        artists_ids = list(set([
            artist.id for track in tracks for artist in track.artists
        ]))

        artists = self.get_artists(artist_ids=artists_ids)
        artists = {artist.id: artist for artist in artists}

        for track in tracks:
            for artist in track.artists:
                artist.genres = artists[artist.id].genres
                artist.popularity = artists[artist.id].popularity

        return tracks
