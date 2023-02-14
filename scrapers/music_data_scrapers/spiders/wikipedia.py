import scrapy

from scrapers.music_data_scrapers.items import MusicDataScrapersItem
from recommender_system.data_engineering.data_provider import DataProvider


class Wikipedia(scrapy.Spider):
    name = "wikipedia"
    
    allowed_domains = [
        'wikipedia.com',
        'en.wikipedia.org',
        'wikipedia.org'
    ]
    
    wikipedia_root_pages = [
        "https://en.wikipedia.org/wiki/List_of_music_genres_and_styles",
        "https://en.wikipedia.org/wiki/List_of_electronic_music_genres",
        "https://en.wikipedia.org/wiki/Lists_of_musicians"
    ]
    
    base_url="https://en.wikipedia.org"
    
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
        for url in self.wikipedia_root_pages:
            yield scrapy.Request(url=url,method='GET')


    def parse(self, response):
        music_genres_url = response.xpath('//div[@class="mw-parser-output"]/div//li/a/@href').getall()
        for genre_url in music_genres_url:
            yield scrapy.Request(
                url=self.base_url + genre_url,
                method='GET',
                callback=self.parse_genre_article
            )
    
    
    def parse_genre_article(self, response):
        artist_entities_identified = response.xpath('//p/a/text()').getall()
        
        artists_tagged = MusicDataScrapersItem()
        
        artists_tagged['url'] = response.request.url
        artists_tagged['artists'] = []
        
        for artist in artist_entities_identified:
            artist_object = self.data_provider.artist_mapper(artist)
            
            if artist_object is not None and artist_object.id not in artists_tagged['artists']:
                artists_tagged['artists'].append(artist_object.id)
        
        yield artists_tagged
        