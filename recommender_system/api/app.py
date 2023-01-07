from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from recommender_system.musicos import MusicOs


app = FastAPI()

musicos = MusicOs()


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url='/docs')


@app.get("/recommendations_for_playlist/{playlist_id}")
async def recommendations_for_playlist(playlist_id: str):
    
    musicos.recommend_k_tracks_for_playlist(
        playlist_id=playlist_id,
        output_playlist_id="3RNUyOGbClap09tyDtLb8R",
        add_to_spotify_playlist=True
    )