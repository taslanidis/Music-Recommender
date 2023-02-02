from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from recommender_system.musicos import MusicOs


app = FastAPI()
musicos = MusicOs()


@app.on_event("startup")
async def startup_event():
    musicos.reset_session()


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url='/docs')


@app.get("/recommendations_for_playlist/{playlist_id}")
async def recommendations_for_playlist(playlist_id: str):
    """Get recommendation for specific playlist
    """
    return musicos.recommend_k_tracks_for_playlist(
        playlist_id=playlist_id,
        output_playlist_id="3RNUyOGbClap09tyDtLb8R",
        add_to_spotify_playlist=True
    )


@app.get("/session/add/{playlist_id}")
async def session_add(playlist_id: str):
    """Add playlist to session
    """
    musicos.add_playlist_to_session(
        playlist_id=playlist_id
    )


@app.get("/session/recommendations")
async def recommendations_for_session():
    """Get recommendations for the current session
    """
    return musicos.generate_session_recommendations(
        output_playlist_id="3RNUyOGbClap09tyDtLb8R",
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