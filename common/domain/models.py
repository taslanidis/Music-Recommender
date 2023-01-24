from typing import Dict


# These are the models that will be used internally by our models

class Track:
    Popularity: float = None
    Danceability: float = None
    
    _attrs_to_normalize = [
        'Popularity',
        'Danceability'
    ]
    
    
    def get_normalizable_part(self) -> Dict:
        return {
            key: getattr(self, key) for key in self._attrs_to_normalize
        }



class Artist:
    pass