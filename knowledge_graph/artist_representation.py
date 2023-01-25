from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize

import re

w2v_artist_features = 16


class ArtistRepresentationModel:

    def __init__(self):
        # load models
        self._artist_emb_model = Word2Vec.load("./models/artist_embedding_v1.model")

        # PCA for dimensionality reduction
        track_artist_embeddings = [
            artist_emb_model.wv[artists[0].strip()] if artists[0].strip() in artist_emb_model.wv else np.array([np.nan] * w2v_artist_features)
                for artists in tqdm(df_db_tracks['id_artists'], desc="tracks")
        ]

        self._pca_model = PCA(n_components=6)
        self._pca_model.fit(track_artist_embeddings)


    def embedding_normalizer(self, embeddings, fillna: Optional[bool] = False):
        embeddings = np.array(embeddings)
        embeddings = artist_embeddings_scaler.transform(embeddings)

        if fillna:
            embeddings = np.nan_to_num(embeddings, nan=-1.0)
