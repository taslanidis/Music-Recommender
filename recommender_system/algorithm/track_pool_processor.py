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
        user_track_dict: Dict[str, List[Track]]
    ) -> Dict[str, TrackPoolItem]:
        """
        {
            User ID i ---> [ List of suggested tracks i ],
            User ID j ---> [ List of suggested tracks j ]
        }

        [ List of suggested tracks ] consists of L tracks, each contributing with a specific weight.

        For each user, weights add to 1
        Ui --> [0.5 0.5]
        Uj --> [0.33 0.33 0.33]

        Merge all bins and create a set of TrackID -> (Frequency, Track),
            where frequency is the sum of all frequencies for same tracks existing in different bins

        Finally,

        T1 --> f1
        T2 --> f2
        T3 --> f3
        """
        track_pool_items: Dict[str, TrackPoolItem] = {}

        for _, user_items in user_track_dict.items():
            
            user_dict_items: Dict[str, Track] = {
                track.id: track for track in user_items
            }
            bin_total_tracks = len(user_dict_items)
            
            count = Counter(list(user_dict_items.keys()))
            
            for track_id, freq in count.items():

                if track_id not in track_pool_items:    
                    
                    track_pool_items[track_id] = TrackPoolItem(
                        track=user_dict_items[track_id],
                        frequency=freq/bin_total_tracks # probability based frequency xi / N
                    )

                else:

                    track_pool_items[track_id].frequency += freq/bin_total_tracks # probability based frequency xi / N

        return track_pool_items
