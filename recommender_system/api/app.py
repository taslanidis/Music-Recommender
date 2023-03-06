from fastapi import FastAPI
from fastapi.responses import RedirectResponse, JSONResponse
from typing import Optional

from recommender_system.musicos import MusicOs
from common.data_transfer.models import SessionSettings, SessionAddition
from common import utils


app = FastAPI()
musicos = MusicOs()


@app.on_event("startup")
async def startup_event():
    musicos.reset_session()


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url='/docs')


@app.post("/recommendations_for_playlist")
async def recommendations_for_playlist(
    playlist_id: str, 
    settings: Optional[SessionSettings]
):
    """Get recommendation for specific playlist

    Playlist ID can be both ID or playlist link
    """
    is_playlist, is_track, playlist_id = utils.get_spotify_object_id(playlist_id)
    
    if is_track:
        return JSONResponse(status_code=400, content="Invalid <playlist_id>")

    return musicos.recommend_k_tracks_for_playlist(
        playlist_id=playlist_id,
        output_playlist_id="3RNUyOGbClap09tyDtLb8R",
        settings=settings,
        add_to_spotify_playlist=True
    )


@app.post("/session/add")
async def session_add(session_addition: SessionAddition):
    """Add playlist to session

    Playlist ID can be both ID or playlist link
    """
    is_playlist, is_track, object_id = utils.get_spotify_object_id(session_addition.playlist_or_track_id)

    if is_playlist:
        musicos.add_playlist_to_session(
            playlist_id=object_id,
            user_id=session_addition.provided_by_user_id
        )
        
    elif is_track:
        musicos.add_track_to_session(
            track_id=object_id,
            user_id=session_addition.provided_by_user_id
        )
    
    else:
        return JSONResponse(status_code=400, content="Invalid <playlist_or_track_id>") 
    


@app.post("/session/recommendations")
async def recommendations_for_session(settings: Optional[SessionSettings] = None):
    """Get recommendations for the current session
    """
    return musicos.generate_session_recommendations(
        output_playlist_id="3RNUyOGbClap09tyDtLb8R",
        settings=settings,
        add_to_spotify_playlist=True
    )


@app.get("/session/statistics")
async def session_stats():
    """Get session statistics
    """
    return musicos.get_session_stats()


@app.get("/session/clustering/plot")
async def session_clusters():
    """Get session clusters for plot
    """
    return musicos.get_track_pool_clusters()


@app.get("/session/reset")
async def reset_session():
    musicos.reset_session()