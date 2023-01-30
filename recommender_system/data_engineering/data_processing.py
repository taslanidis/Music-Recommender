import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from typing import List, Dict
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
        self._genre_embeddings = Word2Vec.load(self._settings.genre_embeddings)
        self._artist_embeddings = Word2Vec.load(self._settings.artist_embeddings)
        self._tfidf = TfidfVectorizer(tokenizer=word_tokenize)
        self.w2v_genre_features = self._settings.genre_embeddings_size
        self.w2v_artist_features = self._settings.artist_embeddings_size
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
        track: Track,
        tf_idf_features
    ) -> RepresentationVector:
        """Internal creator of track representation vectors

        Args:
            track (Track): track domain model
            tf_idf_features (_type_): tf idf feature names

        Returns:
            RepresentationVector: output representation vector
        """
        concatenated_genres = " ".join([self.process_genre(genre) for genre in track.genres])
            
        genre_embedding = self.create_sentence_embedding(
            sentence_tokenized=word_tokenize(concatenated_genres),
            weights_per_word=self._tfidf.transform([concatenated_genres]).toarray().reshape(-1,), 
            tfidf_vocab=tf_idf_features,
            features_number=self.w2v_genre_features
        )
        
        artist_embedding = np.array([np.nan] * self.w2v_artist_features)
        
        if track.id_artists[0].strip() in self._artist_embeddings.wv:
            artist_embedding = self._artist_embeddings.wv[track.id_artists[0].strip()] 

        # combine information in a single vector
        representation_vector = np.hstack(
            [
                self.normalize_features(track),
                genre_embedding,
                artist_embedding
            ]
        )
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
        vocab = list(set(
            [
                token for track in tqdm(tracks, desc="Creating vocab for genres") \
                    for genre in track.genres \
                    for token in word_tokenize(self.process_genre(genre))
            ]
        ))
        self._tfidf.fit(vocab)
        tf_idf_features = list(self._tfidf.get_feature_names_out())
        
        representation_vectors = {}
        for track in tqdm(tracks, desc="Creating Track Vectors"):
            representation_vector = self._create_track_representation_vector(
                track = track,
                tf_idf_features = tf_idf_features
            )
            representation_vectors[track.id] = representation_vector
            
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
            track = track,
            tf_idf_features = list(self._tfidf.get_feature_names_out())
        )
    
    
    def process_genre(self, genre: str) -> str:
        new_genre = genre.replace('hip hop', 'hiphop')
        new_genre = genre.replace('r&b', 'rb')
        return new_genre.strip()


    def create_sentence_embedding(
        self,
        sentence_tokenized: List[str],
        weights_per_word: NDArray,
        tfidf_vocab,
        features_number: int
    ) -> NDArray:
        """Creates a sentence embedding based on multiple tokens.

        Args:
            sentence_tokenized (List[str]): _description_
            weights_per_word (NDArray): _description_
            tfidf_vocab (_type_): _description_
            features_number (int): _description_

        Returns:
            NDArray: Sentence embedding
        """
        sentence_vector = np.zeros(features_number,)
        for word in sentence_tokenized:
            weight = weights_per_word[tfidf_vocab.index(word)]
            word_vector = self._genre_embeddings.wv[word]
            word_vector = word_vector * weight
            sentence_vector += word_vector

        return sentence_vector / len(sentence_tokenized) if len(sentence_tokenized) > 0 else np.array([np.nan]*features_number)
