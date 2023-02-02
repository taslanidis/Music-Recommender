import numpy as np

from numpy.typing import NDArray
from typing import List, get_type_hints, Tuple
from sklearn.cluster import DBSCAN
from sklearn.manifold import TSNE

from common.domain.models import Track, RepresentationVector


class ProfileCreator:
    """Profile Creator
    
    Creates an eigen vector (representation vector) for a large set of vectors.
    The final vectors will be the representatives of the set.
    
    On this implementation it is done with DBSCAN.
    
    Using hierarchial clustering (DBSCAN) can identify different groups distinctly characterized.
    N-clusters identified, will provide us with N-centroids which will be used as N-representatives. 
    """


    def __init__(self):
        self._profiler = DBSCAN(
            eps=0.1, 
            metric='cosine', 
            min_samples=5
        )


    def create_profile_for_track_pool(
        self,
        tracks: List[RepresentationVector]
    ) -> List[RepresentationVector]:
        """Representation vector creation

        Args:
            tracks (List[Track]): a set of tracks which will be later described by the representation vectors

        Returns:
            List[Track]: a set of representation vectors for all distinct groups in track pool
        """
        cluster_result = self._profiler.fit_predict(
            tracks
        )
        
        points_per_cluster = {}
        for i, cluster in enumerate(cluster_result):
            if cluster not in points_per_cluster:
                points_per_cluster[cluster] = []
            points_per_cluster[cluster].append(tracks[i])
        
        representation_vectors = []
        for cluster in points_per_cluster.keys():
            representation_vectors.append(
                np.mean(
                    np.array(points_per_cluster[cluster]), 
                    axis=0
                )
            )
        
        return representation_vectors
    
    
    def get_tsne_points_with_cluster(
        self, 
        tracks: List[RepresentationVector]
    ) -> List[Tuple[NDArray, int]]:
        
        cluster_result = self._profiler.fit_predict(
            tracks
        )
    
        tsne_model = TSNE(perplexity=10, n_components=2, init='pca', n_iter=2500, random_state=23)
        tsne_reduced_output = tsne_model.fit_transform(tracks)
        
        return list(zip(tsne_reduced_output, cluster_result))
