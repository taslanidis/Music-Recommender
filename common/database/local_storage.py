import pandas as pd

from typing import List
from settings import get_settings

from common.database.default_db import DefaultDb
from common.domain.models import Artist, Track


class LocalStorage(DefaultDb):
    
    def __init__(self):
        self._settings = get_settings()
        self._track_path = self._settings.track_local_stored_path
        self._artist_path = self._settings.artist_local_stored_path
    
    
    def load_all_tracks(self) -> List[Track]:
        df_db_tracks = pd.read_csv(self._track_path)
        df_db_tracks['id_artists'] = df_db_tracks['id_artists'].apply(lambda x: x[1:-1].strip().replace("'", "").split(','))
        return [Track(**track) for track in df_db_tracks.to_dict('records')]


    def load_all_artists(self) -> List[Artist]:
        df_db_artists = pd.read_csv('../dataset/artists.csv')
        df_db_artists['genres'] = df_db_artists['genres'].apply(lambda x: x[1:-1].strip().replace("'", "").split(','))
        return [Artist(**artist) for artist in df_db_artists.to_dict('records')]