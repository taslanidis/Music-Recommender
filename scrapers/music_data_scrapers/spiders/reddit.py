import scrapy

from scrapers.music_data_scrapers.items import MusicDataScrapersItem
from recommender_system.data_engineering.data_provider import DataProvider


class Reddit(scrapy.Spider):
    name = "reddit"
    
    allowed_domains = [
        'old.reddit.com',
        'reddit.com',
    ]
    
    reddit_root_pages = [
        "https://old.reddit.com/r/Music/"
    ]
    
    base_url="https://old.reddit.com"
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapers.music_data_scrapers.pipelines.MusicDataScrapersPipeline': 400
        }
    }
    
    data_provider = DataProvider(
        create_hash_map_for_artists=True,
        use_as_mapper_only=True
    )


    def start_requests(self):
        for url in self.reddit_root_pages:
            yield scrapy.Request(url=url,method='GET')


    def parse(self, response):
        pass
        