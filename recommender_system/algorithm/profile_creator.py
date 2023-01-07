import numpy as np

from typing import List, Optional, get_type_hints
from numpy.typing import NDArray
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from common.data_transfer.models import EnhancedTrack, TrackAudioFeatures


class ProfileCreator:

    def __init__(self):
        self._profiler = PCA(
            n_components=1, #TODO: resarch on this
            svd_solver='auto' #TODO: make this parametrizable
        )
        
        self._normalizer = StandardScaler()

        self._profiler_max_features = 6


    def prepare_profiler(
        self,
        fit_data: List[TrackAudioFeatures]
    ):
        self._fit_normalizer(fit_data)
        self._fit_profiler(fit_data)


    def _fit_normalizer(
        self,
        fit_data: List[TrackAudioFeatures]
    ):
        self._normalizer.fit(
            [data_point.to_numpy() for data_point in fit_data]
        )


    def _fit_profiler(
        self,
        fit_data: List[TrackAudioFeatures]
    ):
        data = np.array([data_point.to_numpy() for data_point in fit_data])

        normalized_fit_data = self._normalizer.transform(
            data
        )

        for k in range(len(normalized_fit_data) // self._profiler_max_features + 1):

            batch_normalized_fit_data = np.transpose(normalized_fit_data[k:k+self._profiler_max_features])

            self._profiler.fit(
                batch_normalized_fit_data
            )


    def create_profile_for_track_pool(
        self,
        tracks: List[EnhancedTrack]
    ) -> TrackAudioFeatures:
        """
        Creates the eigen track for a list of tracks
        Just like an eigen vector is for a matrix
        """
        normalized_tracks = self._normalizer.transform(
            [data_point.audio_features.to_numpy() for data_point in tracks]
        )
        
        normalized_tracks = np.transpose(normalized_tracks)

        normalized_track_pool_profile = self._profiler.transform(
            normalized_tracks
        )
        
        normalized_track_pool_profile = np.transpose(normalized_track_pool_profile)

        track_pool_profile = self._normalizer.inverse_transform(
            normalized_track_pool_profile
        )

        fields = get_type_hints(TrackAudioFeatures)
        return TrackAudioFeatures(
            **{
                field_name: value if field_type != int else np.round(value) 
                    for field_name, field_type, value in zip(fields.keys(), fields.values(), track_pool_profile[0])
            }
        )
