import os

from typer import Typer, echo
from recommender_system.musicos import MusicOs
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

from spotify_connectors.spotify_data_loader import SpotifyAPIDataLoader
from scrapers.music_data_scrapers.spiders.wikipedia import Wikipedia


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


@app.command('scrape-wikipedia-artists')
def scrape_wiki():
    settings_file_path = 'scrapers'
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
    process = CrawlerProcess(settings=get_project_settings())

    process.crawl(Wikipedia)
    process.start() # the script will block here until the crawling is finished
    
    
if __name__ == "__main__":
    app()