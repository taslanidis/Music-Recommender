import time

from typing import Optional, List, Dict
from tqdm import tqdm

from spotify_connectors.spotify_web_api import SpotifyWebAPI
from common.database.mongo_db import MongoDatabase
from common.data_transfer.models import Album, Artist, EnhancedTrack, Playlist


class SpotifyAPIDataLoader:

    def __init__(self):
        self.spotify_web_api = SpotifyWebAPI(throughput_limiter=True)
        self.db = MongoDatabase()


    def load_top_k_playlists_per_category(
        self, 
        category_limit: Optional[int] = None, 
        k: Optional[int] = 10,
        spotify_api_holdback_in_seconds: Optional[int] = 1
    ) -> List:

        categories = self.spotify_web_api.get_categories(limit=category_limit)

        playlists: List[Playlist] = []
        
        for category in tqdm(categories, desc="Loading categories", unit="category"):

            category_playlists = self.spotify_web_api.get_playlists_for_category(
                category_id = category.id, 
                limit = k
            )

            for playlist in category_playlists:
                playlists.append(playlist)

        for playlist in tqdm(playlists, desc="Loading playlist tracks", unit="playlist", leave=False):
            self.load_playlist_tracks(playlist_id = playlist.id)
            time.sleep(spotify_api_holdback_in_seconds)


    def load_playlist_tracks(self, playlist_id: str):
        tracks = self.spotify_web_api.get_playlist_tracks(playlist_id = playlist_id)
        
        audio_features = self.spotify_web_api.get_audio_features_for_tracks(
            tracks=[track.id for track in tracks]
        )

        audio_features = {
            track_audio_features.id: track_audio_features for track_audio_features in audio_features
        }

        artists: Dict[str, Artist] = {}
        albums: Dict[str, Album] = {}
        enhanced_tracks: List[EnhancedTrack] = []
        
        for track in tracks:

            if self.db.is_track_in_db(track.id):
                continue

            if track.album.id not in albums:
                albums[track.album.id] = track.album

            for track_artist in track.artists:
                artists[track_artist.id] = track_artist
        
            enhanced_tracks.append(
                EnhancedTrack(audio_features=audio_features[track.id].dict(), **track.dict())
            )

        # store information in mongo
        self.db.upsert_multiple_tracks(enhanced_tracks)
        self.db.upsert_multiple_artists(artists.values())
        self.db.upsert_multiple_albums(albums.values())