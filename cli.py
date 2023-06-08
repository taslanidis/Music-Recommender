import os
import json

from typer import Typer, echo
from recommender_system.musicos import MusicOs
from common.data_transfer.models import SessionSettings, Mode
from spotify_connectors.spotify_web_api import SpotifyWebAPI


app = Typer()


@app.command('recommend-for-playlist')
def recommend_for_playlist(playlist_id: str):
    musicos = MusicOs()
    recommendations = musicos.recommend_k_tracks_for_playlist(
        playlist_id=playlist_id,
        output_playlist_id="3RNUyOGbClap09tyDtLb8R",
        add_to_spotify_playlist=True,
        settings=SessionSettings(include_genres=['dance'])
    )
    echo(recommendations)


@app.command('scrape-wikipedia-artists')
def scrape_wiki():
    from scrapy.utils.project import get_project_settings
    from scrapy.crawler import CrawlerProcess
    from scrapers.music_data_scrapers.spiders.wikipedia import Wikipedia


    settings_file_path = 'scrapers'
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
    process = CrawlerProcess(settings=get_project_settings())

    process.crawl(Wikipedia)
    process.start() # the script will block here until the crawling is finished


@app.command('scrape-concerts')
def scrape_wiki():
    from scrapy.utils.project import get_project_settings
    from scrapy.crawler import CrawlerProcess
    from scrapers.music_data_scrapers.spiders.concerts import Concerts


    settings_file_path = 'scrapers'
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
    process = CrawlerProcess(settings=get_project_settings())

    process.crawl(Concerts)
    process.start() # the script will block here until the crawling is finished


@app.command('scrape-reddit-artists')
def scrape_wiki():
    from scrapy.utils.project import get_project_settings
    from scrapy.crawler import CrawlerProcess
    from scrapers.music_data_scrapers.spiders.reddit import Reddit


    settings_file_path = 'scrapers'
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
    process = CrawlerProcess(settings=get_project_settings())

    process.crawl(Reddit)
    process.start() # the script will block here until the crawling is finished


@app.command('get-enhanced-track')
def get_enhanced_track(track_id: str):
    sp_api = SpotifyWebAPI()
    enhanced_track = sp_api.get_enhanced_track(track_id=track_id)
    echo(json.dumps(enhanced_track.dict(), indent=4, default=str))


@app.command('get-playlist-tracks')
def get_playlist_tracks(playlist_id: str):
    sp_api = SpotifyWebAPI()
    tracks = sp_api.get_playlist_tracks(playlist_id=playlist_id)
    echo(json.dumps(tracks[0].dict(), indent=4, default=str))


@app.command('get-enhanced-track-with-artist')
def get_enhanced_track_with_artist(track_id: str):
    sp_api = SpotifyWebAPI()
    enhanced_track = sp_api.get_enhanced_track(track_id=track_id)
    enhanced_track = sp_api.enhance_tracks_with_artist_information(tracks=[enhanced_track])[0]
    echo(json.dumps(enhanced_track.dict(), indent=4, default=str))


if __name__ == "__main__":
    app()