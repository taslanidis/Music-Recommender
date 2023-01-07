from pymongo import MongoClient, ReplaceOne
from typing import List

from common.data_transfer.models import Album, Artist, EnhancedTrack


class MongoDatabase:

    def __init__(self):
        self.__client = MongoClient('localhost', 27017)
        self.db = self.__client['musicos']
        self.collection_tracks = self.db['Tracks']
        self.collection_artists = self.db['Artists']
        self.collection_albums = self.db['Albums']


    def upsert_multiple_tracks(self, tracks: List[EnhancedTrack]) -> bool:
        operations = [
            ReplaceOne({"id": track.id}, track.dict(), upsert=True) for track in tracks
        ]

        if len(operations) > 0:
            self.collection_tracks.bulk_write(operations)

        return True


    def upsert_multiple_artists(self, artists: List[Artist]) -> bool:
        operations = [
            ReplaceOne({"id": artist.id}, artist.dict(), upsert=True) for artist in artists
        ]

        if len(operations) > 0:
            self.collection_artists.bulk_write(operations)

        return True


    def upsert_multiple_albums(self, albums: List[Album]) -> bool:
        operations = [
            ReplaceOne({"id": album.id}, album.dict(), upsert=True) for album in albums
        ]

        if len(operations) > 0:
            self.collection_albums.bulk_write(operations)

        return True


    def load_all_tracks(self) -> List[EnhancedTrack]:
        cursor = self.collection_tracks.find({})
        return [EnhancedTrack(**track) for track in cursor]


    def load_all_artists(self) -> List[Artist]:
        cursor = self.collection_artists.find({})
        return [Artist(**artist) for artist in cursor]


    def is_track_in_db(self, track_id: str) -> bool:
        cursor = self.collection_tracks.find({'id': track_id})

        if cursor is not None:
            return len(list(cursor)) > 0

        return False


    def disconnect(self):
        self.__client.close()