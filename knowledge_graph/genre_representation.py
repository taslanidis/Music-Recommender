from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize

import re

w2v_genre_features = 16

class GenreRepresentationModel:

    def __init__(self):
        # load models
        self._genre_emb_model = Word2Vec.load("./models/genre_embeddings_v1.model")
        self.custom_vocab = ["piano", "guitar", "rock", "metal", "pop", "folk", "country", "dance", "vintage", "tango", "latin", "classic", "jazz", "lounge", "easy", "blues", "electronic", "ballad", \
        "indie", "electropop", "soul", "comedy", "rap", "alternative", "reggaeton", "reggae", "trap", "punk", "techno", "vocal", "soundtrack", "epic", "house", "deep", \
        "garage", "hiphop", "rb", "uk", "us", "polish", "french", "russian", "edm", "chill", "samba", "downtempo", "greek", "drill", "czsk"]

        vocab = list(set([token for genres in df_db_tracks['genres'].to_list() for genre in genres for token in word_tokenize(process_genre(genre))]))
        genres_text = [" ".join([self.process_genre(genre) for genre in track_genres]) for track_genres in df_db_tracks['genres'].to_list()]

        # TF-IDF model
        self._tfidf = TfidfVectorizer(tokenizer=word_tokenize)
        self._tfidf = tfidf.fit(vocab)

        # PCA for dimensionality reduction
        track_genres_embeddings = [
            create_sentence_embedding(
                sentence_tokenized=word_tokenize(track_genre_text), 
                weights_per_word=tfidf.transform([track_genre_text]).toarray().reshape(-1,), 
                tfidf_vocab=list(tfidf.get_feature_names_out()),
                features_number=w2v_genre_features
            ) 
                for track_genre_text in tqdm(genres_text, desc="tracks")
        ]

        self._pca_model = PCA(n_components=6)
        self._pca_model.fit(track_genres_embeddings)


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
        sentence_vector = np.zeros(features_number,)
        for word in sentence_tokenized:
            weight = weights_per_word[tfidf_vocab.index(word)]
            word_vector = genre_emb_model.wv[word]
            word_vector = word_vector * weight
            sentence_vector += word_vector

        return sentence_vector / len(sentence_tokenized) if len(sentence_tokenized) > 0 else np.array([np.nan]*features_number)
