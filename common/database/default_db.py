from typing import List, Dict

from common.domain.models import Track, Artist


# Default Database wrapper

class DefaultDb:

    def load_tracks(self) -> Dict[str, Track]:
        pass
    
    def load_artists(self) -> Dict[str, Artist]:
        pass
    
    def is_track_in_db(self) -> bool:
        pass