from typing import get_type_hints
from datetime import datetime

from common.data_transfer.models import (
    EnhancedTrack as EnhancedTrackDto,
    Artist as ArtistDto
)
from common.domain.models import (
    Track as Track,
    Artist as Artist
)


class TrackConversionInterface:

    @staticmethod
    def convert_dto_to_domain(track: EnhancedTrackDto) -> Track:
        domain_object_attrs = {}
        for feature in get_type_hints(track.audio_features):
            domain_object_attrs[feature] = getattr(track.audio_features, feature)
        for feature in get_type_hints(track):
            domain_object_attrs[feature] = getattr(track, feature)

        domain_object_attrs['release_date'] = track.album.release_date
        domain_object_attrs['track_age'] = (datetime.today() - track.album.release_date).total_seconds()//(365*24*3600)
        domain_object_attrs['genres'] = self.get_genres_for_artists([artist.id for artist in track.artists])
        domain_object_attrs['artist_popularity'] = self.get_popularity_for_artists([artist.id for artist in track.artists])
        domain_object_attrs['artist_mean_popularity'] = np.nan
        domain_object_attrs['artist_max_popularity'] = np.nan
        
        if len(domain_object_attrs['artist_popularity']) > 0:
            domain_object_attrs['artist_mean_popularity'] = np.mean(domain_object_attrs['artist_popularity'])
            domain_object_attrs['artist_max_popularity'] = np.max(domain_object_attrs['artist_popularity'])
        
        return Track(**domain_object_attrs)


class ArtistConversionInterface:

    @staticmethod
    def convert_dto_to_domain(artist: ArtistDto) -> Artist:
        return Artist(**artist.dict())