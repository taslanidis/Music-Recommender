import pandas as pd
import numpy as np
import os.path

from datetime import datetime
from typing import List, Dict
from settings import get_settings
from tqdm import tqdm

from common.database.default_db import DefaultDb
from common.domain.models import Artist, Track, RepresentationVector


class LocalStorage(DefaultDb):
    
    _artists: Dict[str, Artist] = None
    _tracks: Dict[str, Track] = None
    _track_representation_vectors: Dict[str, RepresentationVector] = None
    _genres_vocab: List[str]

    def __init__(self):
        self._settings = get_settings()
        self._track_path = self._settings.track_local_stored_path
        self._artist_path = self._settings.artist_local_stored_path
        self._genres_vocab_path = self._settings.genre_vocab_local_stored_path
        self._track_representation_vectors_path = self._settings.track_representation_vectors_stored_path
        self._artists = self.load_artists()
        self._tracks = self.load_tracks()
        self._genres_vocab = self.load_genres_vocab()
        self._track_representation_vectors = self.load_track_representation_vectors()
    
    
    def get_all_tracks_csv(self) -> pd.DataFrame:
        """Read local storage CSV file with all tracks
        Then apply necessary processing.
        
        In local storage, the data are stored in CSV
            -> We use pandas to process them

        Returns:
            pd.DataFrame
        """
        df_db_tracks = pd.read_csv(self._track_path)
        df_db_tracks['release_date'] = pd.to_datetime(df_db_tracks['release_date'], yearfirst=True, format='mixed')
        df_db_tracks['id_artists'] = df_db_tracks['id_artists'].apply(
            lambda x: x[1:-1].strip().replace("'", "").split(',')
        )
        return df_db_tracks


    def get_all_artists_csv(self) -> pd.DataFrame:
        """Read local storage CSV file with all artists
        Then apply necessary processing.
        
        In local storage, the data are stored in CSV
            -> We use pandas to process them

        Returns:
            pd.DataFrame
        """
        df_db_artists = pd.read_csv(self._artist_path)
        df_db_artists['genres'] = df_db_artists['genres'].apply(
            lambda x: x[1:-1].strip().replace("'", "").split(',')
        )
        return df_db_artists


    def load_track_representation_vectors(self):
        representation_vectors = pd.read_csv(self._track_representation_vectors_path)
        representation_vectors.set_index('id', inplace=True)
        representation_vectors = representation_vectors.to_dict(orient='index')
        representation_vectors = {
            key: np.array(list(vector.values())) for key, vector in representation_vectors.items()
        }
        return representation_vectors


    def load_genres_vocab(self):
        df = pd.read_csv(self._genres_vocab_path)
        return df['word'].to_list() 


    def load_tracks(self) -> Dict[str, Track]:
        """Load all tracks from local storage DB
        """
        if self._artists is None:
            raise Exception("""Artists are not initialized. 
                            First initialize artists before processing tracks."""
                    )

        df_db_tracks = self.get_all_tracks_csv()
        tracks = df_db_tracks.to_dict(orient='records')
        
        # fill calculated fields for tracks
        for track in tqdm(tracks, desc='Processing tracks'):
            track['genres'] = self.get_genres_for_artists(track['id_artists'])
            track['artist_popularity'] = self.get_popularity_for_artists(track['id_artists'])
            track['name_artists'] = self.get_names_for_artists(track['id_artists'])
            track['artist_mean_popularity'] = np.mean(track['artist_popularity']) if len(track['artist_popularity']) > 0 else np.nan
            track['artist_max_popularity'] = np.max(track['artist_popularity']) if len(track['artist_popularity']) > 0 else np.nan
            track['track_age'] = (datetime.today() - track['release_date']).total_seconds()//(365*24*3600)
        
        return {track['id']: Track(**track) for track in tracks}


    def load_artists(self) -> Dict[str, Artist]:
        """Load all artists from local storage DB

        Returns:
            Dict[str, Artist]: Dictionary with artist_id: Artist
        """
        df_db_artists = self.get_all_artists_csv()
        return {
            record['id']: Artist(**record) for record in tqdm(df_db_artists.to_dict(orient='records'), desc="Processing artists")
        }


    def get_genres_for_artists(
        self, 
        id_artists: List[str]
    ) -> List[str]:
        """Extracting genres for a set of artists

        Args:
            id_artists (List[str]): set of artist ids

        Returns:
            List[str]: The list with the extracted genres. 
                        (It can contain duplicates)
        """
        genres = []
        
        for artist_id in id_artists:
            genres += self._artists[artist_id].genres if artist_id in self._artists else []
        
        return [genre.strip() for genre in genres if genre != ""]


    def get_popularity_for_artists(
        self, 
        id_artists: List[str]
    ) -> List[int]:
        """Extract the popularity for a set of artists

        Args:
            id_artists (List[str]): artist ids

        Returns:
            List[int]: A list with each artist's popularity
        """
        popularity = []
        
        for artist_id in id_artists:
            popularity += [self._artists[artist_id].popularity] if artist_id in self._artists else []
        
        return popularity
    
    
    def get_names_for_artists(
        self,
        id_artists: List[str]
    ) -> List[str]:
        """Extract the names for a set of artists

        Args:
            id_artists (List[str]): artist ids

        Returns:
            List[int]: A list with each artist's name
        """
        names = []
        
        for artist_id in id_artists:
            names += [self._artists[artist_id].name] if artist_id in self._artists else []
        
        return names
    
    
    def get_tracks(self):
        return self._tracks
    
    
    def get_artists(self):
        return self._artists


    def get_genres_vocab(self):
        return self._genres_vocab
    

    def get_track_representation_vectors(self):
        return self._track_representation_vectors
