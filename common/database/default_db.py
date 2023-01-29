from typing import List

from common.domain.models import Track, Artist


# Default Database wrapper

class DefaultDb:

    def load_tracks(self) -> List[Track]:
        pass
    
    def load_artists(self) -> List[Artist]:
        pass
    
    def is_track_in_db(self) -> bool:
        pass