import numpy as np

from typing import List, Optional
from datetime import datetime, date
from dateutil import parser
from enum import Enum

from pydantic import BaseModel, validator


class Artist(BaseModel):
    id: str
    href: str
    name: str
    type: str
    uri: str
    genres: List[str] = None
    name: str
    popularity: Optional[float] = None


class Album(BaseModel):
    id: str
    album_type: str
    artists: List[Artist]
    name: str
    available_markets: List[str]
    release_date: datetime
    release_date_precision: str
    total_tracks: int
    uri: str

    @validator("release_date", pre=True)
    def dt(cls, value):
        
        if type(value) == str:
            value = parser.parse(value)

        if isinstance(value, date):
            return datetime.combine(value, datetime.min.time())
        
        return value


class Category(BaseModel):
    id: str
    name: str
    href: str


class TrackAudioFeatures(BaseModel):
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    duration_ms: int
    time_signature: int
    
    def to_numpy(self, exclude=None):
        return np.array(
            list(
                self.dict(exclude=exclude).values()
            )
        )


class TrackAudioFeaturesWithId(TrackAudioFeatures):
    id: Optional[str]

    def to_numpy(self):
        return super().to_numpy(exclude={'id'})


class Track(BaseModel):
    href: str
    id: str
    name: str
    popularity: float
    album: Album
    artists: List[Artist]
    available_markets: List[str]
    disc_number: int
    duration_ms: int
    uri: str
    type: str


class EnhancedTrack(Track):
    audio_features: TrackAudioFeatures


class PlaylistOwner(BaseModel):
    display_name: str
    href: str
    id: str
    type: str
    uri: str


class PlaylistTracksInformation(BaseModel):
    href: str
    total: int


class Playlist(BaseModel):
    href: str
    id: str
    name: str
    owner: PlaylistOwner
    description: str
    type: str
    uri: str
    tracks: PlaylistTracksInformation


class Mode(Enum):
    High = 1
    Mid = 2
    Low = 3
    Undefined = 4

    
class SessionSettings(BaseModel):
    danceability: Optional[Mode] = Mode.Undefined
    energy: Optional[Mode] = Mode.Undefined
    instrumentalness: Optional[Mode] = Mode.Undefined
    speechiness: Optional[Mode] = Mode.Undefined
    valence: Optional[Mode] = Mode.Undefined
    tempo: Optional[Mode] = Mode.Undefined
    include_genres: Optional[List[str]] = None
    exclude_genres: Optional[List[str]] = None
    
    __filters__ = [
        'danceability',
        'energy',
        'instrumentalness',
        'speechiness',
        'valence',
        'tempo',
        'include_genres',
        'exclude_genres'
    ]
    

class SessionAddition(BaseModel):
    playlist_or_track_id: str
    provided_by_user_id: str
