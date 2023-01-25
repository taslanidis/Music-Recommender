from typing import Dict
from sklearn.preprocessing import MinMaxScaler

from common.database.local_storage import LocalStorage


class DataProvider:
    scalers: Dict[str, MinMaxScaler] = None

    def __init__(self):
        self._db = LocalStorage()
        self._tracks: List[Track] = self._db.load_all_tracks()
        self._artists: List[Artist] = self._db.load_all_artists()

        self.scalers = {}


    def normalize_features(self):

        for feature in scaled_features:
            scalers[feature] = MinMaxScaler()
            tempo_array = df_db_tracks[feature].to_numpy()
            tempo_array = tempo_array.reshape(-1,1)
            df_db_track_with_genres[feature] = scalers[feature].fit_transform(tempo_array)