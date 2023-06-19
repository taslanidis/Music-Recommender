import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from typing import List, Dict, Optional
from numpy.typing import NDArray
from tqdm import tqdm

from settings import get_settings
from common.domain.models import Track, RepresentationVector


class DataProcessor:
    """Data Processor
    
    1. Creates track representation vectors.
    2. Normalizes data
    3. Creates embeddings for genres & artists
    """
    scalers: Dict[str, MinMaxScaler] = None
    
    def __init__(self):
        self._settings = get_settings()
        self._genre_embeddings = np.load(self._settings.genre_embeddings, allow_pickle=True)
        self._artist_embeddings = Word2Vec.load(self._settings.artist_embeddings)
        self._tfidf = TfidfVectorizer(tokenizer=word_tokenize)
        self.w2v_genre_features = self._settings.genre_embeddings_size
        self.w2v_artist_features = self._settings.artist_embeddings_size
        self._track_audio_features_weight = 2
        self._track_popularity_weight = 1
        self._track_date_weight = 5
        self._genre_weight = 1
        self._artist_weight = 1
        self.scalers = {}
    
    
    def fit_normalizer(self, tracks: List[Track]) -> None:
        """Fit data to normalizers

        Args:
            tracks (List[Track]): set of track to fit normalizer
        """
        for feature in tqdm(Track.__scaled_features__, desc="Fitting normalizer"):
            self.scalers[feature] = MinMaxScaler()
            feature_array = np.array([getattr(track, feature) for track in tracks]).reshape(-1,1)
            self.scalers[feature].fit(feature_array)
    
    
    def normalize_features(self, track: Track) -> NDArray:
        """Apply normalization for each feature

        Args:
            track (Track): Track object

        Returns:
            NDArray: normalized
        """
        normalized_features = []
        for feature in Track.__scaled_features__:
            normalized_features.append(self.scalers[feature].transform(np.array([getattr(track, feature)]).reshape(1, -1))[0])
        return np.array(normalized_features).reshape(-1,)
    
    
    def _create_track_representation_vector(
        self,
        track: Track
    ) -> Optional[RepresentationVector]:
        """Internal creator of track representation vectors

        Args:
            track (Track): track domain model
            tf_idf_features (_type_): tf idf feature names

        Returns:
            RepresentationVector: output representation vector
        """
        genre_tokens = [self.process_genre(genre) for genre in track.genres]
        
        # if track is of unknown genre - it can not be processed
        if len(genre_tokens) == 0:
            return None
        
        genre_embedding = self.create_sentence_embedding(
            sentence_tokenized=genre_tokens,
            features_number=self.w2v_genre_features
        )
        
        artist_embedding = np.array([np.nan] * self.w2v_artist_features)
        
        if track.id_artists[0].strip() in self._artist_embeddings.wv:
            artist_embedding = self._artist_embeddings.wv.get_vector(track.id_artists[0].strip(), norm=True)

        normalized_features = self.normalize_features(track)
        popularity = normalized_features[track.get_index_of_feature('artist_mean_popularity')]
        track_age = normalized_features[track.get_index_of_feature('track_age')]
        audio_features_vector = np.delete(
            normalized_features,
            [
                track.get_index_of_feature('artist_mean_popularity'),
                track.get_index_of_feature('track_age')
            ]
        )

        # combine information in a single vector
        representation_vector = np.hstack(
            [
                audio_features_vector * self._track_audio_features_weight,
                popularity * self._track_popularity_weight,
                track_age * self._track_date_weight,
                genre_embedding * self._genre_weight,
                artist_embedding * self._artist_weight
            ]
        )

        if np.isnan(representation_vector).any():
            # contains NaN values
            return None

        return representation_vector
    
    
    def _initialize_track_representation_vectors(
        self,
        tracks: List[Track]
    ) -> Dict[str, RepresentationVector]:
        """Generates representation vectors for all tracks.
        
        Combines track info, genre embeddings and artist embeddings.

        Args:
            tracks (List[Track]): set of tracks to create the representation vectors for

        Returns:
            List[RepresentationVector]: List of representation vectors for each track
        """
        try:
            df = pd.read_csv('./dataset/genres_vocab.csv')
            vocab = df['word'].to_list()
        
        except Exception:
        
            vocab = list(set(
                [
                    self.process_genre(genre) \
                        for track in tqdm(tracks, desc="Creating vocab for genres") \
                        for genre in track.genres
                ]
            ))
            
            df = pd.DataFrame(vocab, columns=['word'])
            df.to_csv('./dataset/genres_vocab.csv', index=False)
        
        try:
            representation_vectors = pd.read_csv('./dataset/track_vectors.csv')
            representation_vectors.set_index('id', inplace=True)
            representation_vectors = representation_vectors.to_dict(orient='index')
            representation_vectors = {
                key: np.array(list(vector.values())) for key, vector in representation_vectors.items()
            }
        
        except Exception:
            representation_vectors = {}
            
            for track in tqdm(tracks, desc="Creating Track Vectors"):
                representation_vector = self._create_track_representation_vector(
                    track = track
                )
                
                if representation_vector is not None:
                    representation_vectors[track.id] = representation_vector
                
            df = pd.DataFrame(list(representation_vectors.values()), columns=[f"w{i+1}" for i in range(len(representation_vector))])
            df['id'] = list(representation_vectors.keys())
            df.set_index('id', inplace=True)
            df.to_csv('./dataset/track_vectors.csv')
        
        return representation_vectors
    
    
    def create_track_representation_vector(
        self,
        track: Track
    ) -> RepresentationVector:
        """Wrapper for the internal creator of track representation vectors

        Args:
            track (Track): track domain model

        Returns:
            RepresentationVector: repr output
        """
        return self._create_track_representation_vector(
            track = track
        )
    
    
    def process_genre(self, genre: str) -> str:
        return genre.strip().strip("'")


    def create_sentence_embedding(
        self,
        sentence_tokenized: List[str],
        features_number: int
    ) -> NDArray:
        """Creates a sentence embedding based on multiple tokens.

        Args:
            sentence_tokenized (List[str]): _description_
            features_number (int): _description_

        Returns:
            NDArray: Sentence embedding
        """
        sentence_vector = np.zeros(features_number,)
        tokens_accumulated = 0
        for word in sentence_tokenized:
            
            if word not in self._genre_embeddings.item():
                continue
            
            word_vector = self._genre_embeddings.item().get(word)
            sentence_vector += word_vector
            tokens_accumulated += 1

        return sentence_vector / tokens_accumulated if tokens_accumulated > 0 else np.array([np.nan]*features_number)
