from typing import List, Tuple

from common.domain.models import Track, RecommendedTrack


class MusicCurator:
    
    def curate_recommendation_list(
        self,
        track_pool: List[RecommendedTrack]
    ) -> List[Track]:
        """Curate recommendations based on track information and score

        1. Keeps the same amount of tracks for each category
        2. Deletes all duplicates tracks
        3. Removes very similar tracks, e.g Bicep - Glue, Bicep - Glue Extended, Bicep - Glue Live
            (and keeps only "remixes")

        Args:
            track_pool (List[RecommendedTrack])

        Returns:
            List[Track]: curated recommendations
        """
        pass
        