import pandas as pd

from typing import List
from settings import get_settings
from tqdm import tqdm

from common.database.default_db import DefaultDb
from common.domain.models import Artist, Track


class LocalStorage(DefaultDb):
    
    _artists: Dict[str, Artist] = None
    _tracks: Dict[str, Track] = None

    def __init__(self):
        self._settings = get_settings()
        self._track_path = self._settings.track_local_stored_path
        self._artist_path = self._settings.artist_local_stored_path
        self._artists = self._load_artists()
        self._tracks = self._load_tracks()
    
    
    def get_all_tracks_csv(self) -> pd.DataFrame:
        df_db_tracks = pd.read_csv(self._track_path)
        df_db_tracks['release_date'] = pd.to_datetime(df_db_tracks['release_date'])
        df_db_tracks['id_artists'] = df_db_tracks['id_artists'].apply(lambda x: x[1:-1].strip().replace("'", "").split(','))
        return df_db_tracks


    def get_all_artists_csv(self) -> pd.DataFrame:
        df_db_artists = pd.read_csv('../dataset/artists.csv')
        df_db_artists['genres'] = df_db_artists['genres'].apply(lambda x: x[1:-1].strip().replace("'", "").split(','))
        return df_db_artists


    def load_tracks(self) -> Dict[str, Track]:
        if self._artists is None:
            raise Exception("Artists are not initialized. First initialize artists before processing tracks.")

        df_db_tracks = self.get_all_tracks_csv()
        tracks = df_db_tracks.set_index('id').to_dict(orient='index')
        
        # fill calculated fields for tracks
        for track in tqdm(tracks, desc='Processing tracks'):
            track['genres'] = self.get_genres_for_artists(tracks['id_artists'])
            track['artist_popularity'] = self.get_popularity_for_artists(track['id_artists'])
            track['artist_mean_popularity'] = np.mean(track['artist_popularity']) if len(track['artist_popularity']) > 0 else np.nan
            track['artist_max_popularity'] = np.max(track['artist_popularity']) if len(x) > 0 else np.nan
            track['track_age'] = (datetime.today() - track['release_date']).total_seconds()//(365*24*3600)
        
        return track


    def load_artists(self) -> Dict[str, Artist]:
        df_db_artists = self.get_all_artists_csv()
        return df_db_artists.set_index('id').to_dict(orient='index')


    def get_genres_for_artists(
        self, 
        id_artists: List[str]
    ) -> List[str]:

        genres = []
        for artist_id in id_artists:
            genres += self._artists[artist_id]['genres'] if artist_id in self._artists.keys() else []
        return list(set(genres))


    def get_popularity_for_artists(
        self, 
        id_artists: List[str]
    ) -> List[int]:

        popularity = []
        for artist_id in id_artists:
            popularity += [self._artists[artist_id]['popularity']] if artist_id in self._artists.keys() else []
        return popularity
