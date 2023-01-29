import numpy as np

from typing import List, get_type_hints
from sklearn.cluster import DBSCAN

from common.domain.models import Track


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
        tracks: List[Track]
    ) -> List[Track]:
        """Representation vector creation

        Args:
            tracks (List[Track]): a set of tracks which will be later described by the representation vectors

        Returns:
            List[Track]: a set of representation vectors for all distinct groups in track pool
        """
        cluster_result = self._profiler.fit_predict(
            tracks
        )
        
        # TODO: find centroids from clusters
        cluster_ids = list(set(cluster_result))
        centroids = []
        for cluster_id in cluster_ids:
            cluster_points = []
            for cluster in cluster_result:
                if track[cluster]
        # TODO: return centroids
        representation_vectors = ...
        
        return representation_vectors
