from typing import Dict
from sklearn.preprocessing import MinMaxScaler

from common.database.local_storage import LocalStorage
from common.domain.models import Track


class DataProvider:

    scalers: Dict[str, MinMaxScaler] = None

    def __init__(self):
        self._db = LocalStorage()
        self._tracks: List[Track] = self._db.load_all_tracks()
        self._artists: List[Artist] = self._db.load_all_artists()
        self.scalers = {}

    
    def _prepare_normalizer(self):
        for feature in Track.scaled_features:
            scalers[feature] = MinMaxScaler()
            feature_array = np.array([getattr(track, feature) for track in self._tracks]).reshape(-1,1)
            scalers[feature].fit(feature_array)


    def get_all_available_tracks(self):
        return self._tracks


    def get_all_available_artists(self):
        return self._artists


    def normalize_features(self):

        for feature in Track.scaled_features:
            tempo_array = df_db_tracks[feature].to_numpy()
            tempo_array = tempo_array.reshape(-1,1)
            df_db_track_with_genres[feature] = scalers[feature].transform(tempo_array)