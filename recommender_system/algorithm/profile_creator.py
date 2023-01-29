import numpy as np

from typing import List, get_type_hints
from sklearn.cluster import DBSCAN

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
                    axis=2
                )
            )
        
        return representation_vectors
