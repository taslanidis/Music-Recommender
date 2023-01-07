from typing import List
from numpy.typing import NDArray
from sklearn.preprocessing import MinMaxScaler

from common.data_transfer.models import EnhancedTrack


class BasicProcessor:

    def __init__(
        self,
        scaler_type = MinMaxScaler
    ):
        self._scaler_type = scaler_type
        self._scalers_per_variable = {}
    

    def create_track_vector_from_enhanced_track(
        self,
        tracks: List[EnhancedTrack]
    ) -> NDArray:
        
        for track in tracks:
            pass
        
        return