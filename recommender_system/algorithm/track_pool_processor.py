from typing import List, Dict
from collections import Counter

from common.domain.models import Track, TrackPoolItem


class TrackPoolProcessor:

    @staticmethod
    def create_track_pool_from_list(
        track_list: List[Track]
    ) -> Dict[str, TrackPoolItem]:
        
        track_dict = {track.id: track for track in track_list}
        track_ids = [track.id for track in track_list]
        total_tracks = len(track_list)
        
        count = Counter(track_ids)
        
        track_pool: Dict[str, TrackPoolItem] = {}
        
        for track_id, freq in count.items():
            track_pool[track_id] = TrackPoolItem(
                track=track_dict[track_id],
                frequency=freq/total_tracks # probability based frequency xi / N
            )
        
        return track_pool
    
    @staticmethod
    def create_track_pool_from_dict(
        track_dict: Dict[str, List[Track]]
    ) -> Dict[str, TrackPoolItem]:
        pass