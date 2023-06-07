from typing import List, Tuple

from common.domain.models import Track, RecommendedTrack
from common.data_transfer.models import SessionSettings, Mode


class SettingsFilter:

    danceability: Tuple[float, float]
    energy: Tuple[float, float]
    instrumentalness: Tuple[float, float]
    speechiness: Tuple[float, float]
    valence: Tuple[float, float]
    tempo: Tuple[float, float]
    include_genres: List[str] = None
    exclude_genres: List[str] = None

    __range_filters__ = [
        'danceability',
        'energy',
        'instrumentalness',
        'speechiness',
        'valence',
        'tempo'
    ]

    def __init__(
        self, 
        session_settings: SessionSettings
    ):
        self.include_genres = session_settings.include_genres \
                                if session_settings.include_genres is not None else []
        self.exclude_genres = session_settings.exclude_genres \
                                if session_settings.exclude_genres is not None else []

        mode = session_settings.danceability
        
        if mode == Mode.High:
            self.danceability = [0.65, 1]
        elif mode == Mode.Mid:
            self.danceability = [0.5, 0.65]
        elif mode == Mode.Low:
            self.danceability = [0.0, 0.5]
        else:
            self.danceability = [0.0, 1.0]

        mode = session_settings.energy

        if mode == Mode.High:
            self.energy = [0.65, 1]
        elif mode == Mode.Mid:
            self.energy = [0.5, 0.65]
        elif mode == Mode.Low:
            self.energy = [0.0, 0.5]
        else:
            self.energy = [0.0, 1.0]

        
        mode = session_settings.valence

        if mode == Mode.High:
            self.valence = [0.6, 1]
        elif mode == Mode.Mid:
            self.valence = [0.45, 0.6]
        elif mode == Mode.Low:
            self.valence = [0.0, 0.45]
        else:
            self.valence = [0.0, 1.0]

        
        mode = session_settings.instrumentalness

        if mode == Mode.High:
            self.instrumentalness = [0.6, 1]
        elif mode == Mode.Mid:
            self.instrumentalness = [0.3, 0.6]
        elif mode == Mode.Low:
            self.instrumentalness = [0.0, 0.3]
        else:
            self.instrumentalness = [0.0, 1.0]


    def __abides(self, track: Track) -> bool:
        if not (self.danceability[0] <= track.danceability <= self.danceability[1]):
            return False

        if not (self.energy[0] <= track.energy <= self.energy[1]):
            return False
        
        if not (self.valence[0] <= track.valence <= self.valence[1]):
            return False
        
        if not (self.instrumentalness[0] <= track.instrumentalness <= self.instrumentalness[1]):
            return False
        
        track_genres = ", ".join(track.genres).lower()

        for genre in self.include_genres:
            
            if track_genres.find(genre.lower()) == -1:
                return False
            
        for genre in self.exclude_genres:
            
            if track_genres.find(genre.lower()) != -1:
                return False
        
        return True 


    def filter(
        self, 
        recommendation_list: List[RecommendedTrack]
    ) -> List[RecommendedTrack]:
        return [recommendation for recommendation in recommendation_list if self.__abides(recommendation.track)]