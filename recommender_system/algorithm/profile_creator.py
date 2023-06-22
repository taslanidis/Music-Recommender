import numpy as np

from numpy.typing import NDArray
from typing import List, get_type_hints, Tuple, Dict, Optional
from sklearn.cluster import DBSCAN
from sklearn.manifold import TSNE
from sklearn.neighbors import NearestNeighbors

from common.domain.models import Track, RepresentationVector, TrackPoolItem


class ProfileCreator:
    """Profile Creator
    
    Creates an eigen vector (representation vector) for a large set of vectors.
    The final vectors will be the representatives of the set.
    
    On this implementation it is done with DBSCAN.
    
    Using hierarchial clustering (DBSCAN) can identify different groups distinctly characterized.
    N-clusters identified, will provide us with N-centroids which will be used as N-representatives. 
    """


    def __init__(self):

        self._dimensionality_reducer = TSNE(
            perplexity=4, 
            n_components=2, 
            init='pca', 
            metric='cosine',
            n_iter=1000, 
            random_state=23
        )


    def _determine_eps(self, data, min_samples: int = 4) -> float:
        # determine eps
        nbrs = NearestNeighbors(n_neighbors=min_samples).fit(data)
        distances, indices = nbrs.kneighbors(data)
        distances = distances[:,2]
        distances = np.sort(distances, axis=0)

        return np.percentile(distances, 95) + 0.2 * np.percentile(distances, 95)


    def create_profile_for_track_pool(
        self,
        track_vectors: Dict[str, RepresentationVector],
        track_pool: Dict[str, TrackPoolItem]
    ) -> Tuple[List[RepresentationVector], List[float]]:
        """Representation vector creation

        Args:
            tracks (List[Track]): a set of tracks which will be later described by the representation vectors

        Returns:
            Tuple[List[Track], List[float]]: a set of representation vectors for all distinct groups in track pool, along with their weights [0-1]
        """
        track_vectors_ids = list(track_vectors.keys())

        track_reduced_vectors = self._dimensionality_reducer.fit_transform(
            np.array(list(track_vectors.values()))
        )

        eps = self._determine_eps(
            data=track_reduced_vectors,
            min_samples=4
        )

        custom_profiler = DBSCAN(
            eps=eps, 
            min_samples=4
        )

        cluster_result = custom_profiler.fit_predict(
            track_reduced_vectors
        )
        
        points_per_cluster: Dict[int, List] = {}
        weights_per_cluster: Dict[int, List] = {}
        
        for i, cluster in enumerate(cluster_result):
            
            # skip outliers (flagged by DBSCAN)
            if cluster == -1: continue
            
            track_id = track_vectors_ids[i]
            
            if cluster not in points_per_cluster:
                points_per_cluster[cluster] = []
                weights_per_cluster[cluster] = []
                
            points_per_cluster[cluster].append(track_vectors[track_id])
            weights_per_cluster[cluster].append(track_pool[track_id].frequency)
        
        representation_vectors = []
        profile_weights = []
        sum_of_freq = np.sum([w for cluster_weights in weights_per_cluster.values() for w in cluster_weights])
        for cluster in points_per_cluster.keys():
            # sum track weights of cluster / sum of all weights
            profile_weights.append(
                np.sum(weights_per_cluster[cluster]) / sum_of_freq
            )
            # Weighted average of track features based on frequencies
            representation_vectors.append(
                np.average(
                    np.array(points_per_cluster[cluster]), 
                    weights=np.array(weights_per_cluster[cluster]),
                    axis=0
                )
            )
        
        return representation_vectors, profile_weights
    
    
    def get_tsne_points_with_cluster(
        self, 
        tracks: List[RepresentationVector]
    ) -> List[Tuple[NDArray, int]]:
        
        representation_vectors = [vector for vector in tracks if vector is not None]

        track_reduced_vectors: NDArray = self._dimensionality_reducer.fit_transform(
            np.array(representation_vectors)
        )

        eps = self._determine_eps(
            data=track_reduced_vectors,
            min_samples=4
        )

        custom_profiler = DBSCAN(
            eps=eps, 
            min_samples=4
        )

        cluster_result = custom_profiler.fit_predict(
            track_reduced_vectors
        )
        
        return list(zip(track_reduced_vectors.tolist(), cluster_result.tolist()))
