from typing import List, Tuple, Optional

from common.domain.models import Track, RecommendedTrack


class MusicCurator:
    
    def curate_recommendation_list(
        self,
        track_pool: List[RecommendedTrack],
        recommendation_number: Optional[int] = 30
    ) -> List[RecommendedTrack]:
        """Curate recommendations based on track information and score

        1. Keeps the same amount of tracks for each category
        2. Deletes all duplicates tracks
        3. Removes very similar tracks, e.g Bicep - Glue, Bicep - Glue Extended, Bicep - Glue Live
            (and keeps only "remixes")

        Args:
            track_pool (List[RecommendedTrack])

        Returns:
            List[RecommendedTrack]: curated recommendations
        """
        sorted_track_pool = sorted(track_pool, key=lambda x: x.score, reverse=False)
        curated_recommendations = []
        categories_stats = {}
        
        max_tracks_per_category = self._get_max_tracks_per_category(
            track_pool=sorted_track_pool,
            recommendation_number=recommendation_number
        )
        
        for track in sorted_track_pool:
            
            if track.category not in categories_stats:
                categories_stats[track.category] = 0
            
            is_already_added = self.check_for_another_track_version_in_list(track.track, curated_recommendations)
            
            if is_already_added:
                continue
            
            if categories_stats[track.category] < max_tracks_per_category:
                curated_recommendations.append(track)
                categories_stats[track.category] += 1
                
        return curated_recommendations
            
            
    def check_for_another_track_version_in_list(
        self,
        track: Track,
        track_list: List[RecommendedTrack]
    ) -> bool:
        """Checks whether another very similar version of a track is already in list

        This algorithm considers remixes different editions of the song.

        Args:
            track (Track): track
            track_list (List[Track]): list of tracks

        Returns:
            bool: track exists in list. False that the track does not exists in list, True that it exsists
        """
        
        for ctrack in track_list:
            # first check ids - most important for duplicates
            if track.id == ctrack.track.id:
                return True
            
            artist_check = False
            
            if ctrack.track.name_artists[0].lower() == track.name_artists[0].lower():
                artist_check = True
            
            track_name_1 = track.name.split("-")[0].lower().strip()
            track_name_2 = ctrack.track.name.split("-")[0].lower().strip()
            
            if artist_check and track_name_1 == track_name_2:
                is_track_1_remix = False
                is_track_2_remix = False
                
                if track.name.find("-") != -1:
                    track_1_edition = track.name.split("-")[1]
                    is_track_1_remix = track_1_edition.lower().find("remix") != -1
                
                if ctrack.track.name.find("-") != -1:
                    track_2_edition = ctrack.track.name.split("-")[1]
                    is_track_2_remix = track_2_edition.lower().find("remix") != -1
                
                if is_track_1_remix or is_track_2_remix:
                    return False
                
                return True
            
        return False
    
    
    def _get_max_tracks_per_category(
        self,
        track_pool: List[RecommendedTrack],
        recommendation_number: int
    ) -> int:
        num_categories = len(list(set([s.category for s in track_pool])))
        return recommendation_number // num_categories + int(recommendation_number % num_categories != 0)
        