from typer import Typer, echo
from recommender_system.musicos import MusicOs

from spotify_connectors.spotify_data_loader import SpotifyAPIDataLoader

app = Typer()


@app.command('load-categories')
def scrape_categories(category_limit: int, top_playlists: int):
    spotify_scraper = SpotifyAPIDataLoader()
    spotify_scraper.load_top_k_playlists_per_category(
        category_limit=category_limit, 
        k=top_playlists,
        spotify_api_holdback_in_seconds=120
    )


@app.command('recommend-for-playlist')
def recommend_for_playlist(playlist_id: str):
    musicos = MusicOs()
    recommendations = musicos.recommend_k_tracks_for_playlist(
        playlist_id=playlist_id,
        output_playlist_id="3RNUyOGbClap09tyDtLb8R",
        add_to_spotify_playlist=True
    )
    echo(recommendations)


if __name__ == "__main__":
    app()