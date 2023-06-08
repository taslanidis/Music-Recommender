import scrapy

from scrapers.music_data_scrapers.items import MusicDataScrapersItem
from recommender_system.data_engineering.data_provider import DataProvider


class Concerts(scrapy.Spider):
    name = "concerts"
    
    allowed_domains = [
        'wikipedia.com',
        'en.wikipedia.org',
        'wikipedia.org'
    ]
    
    wikipedia_root_pages = [
        "https://en.wikipedia.org/wiki/Category:2000s_concert_tours",
        "https://en.wikipedia.org/wiki/Category:2010s_concert_tours",
        "https://en.wikipedia.org/wiki/Category:2020s_concert_tours",
        "https://en.wikipedia.org/wiki/Category:1990s_concert_tours",
        "https://en.wikipedia.org/wiki/Category:1980s_concert_tours"
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
        yearly_concerts_url = response.xpath('//div[@class="mw-category-generated"]//div//li//div/a/@href').getall()
        for year_url in yearly_concerts_url:
            yield scrapy.Request(
                url=self.base_url + year_url,
                method='GET',
                callback=self.parse_yearly_concerts
            )

    
    def parse_yearly_concerts(self, response):
        yearly_concerts_url = response.xpath('//div[@class="mw-category-generated"]/div//li/a/@href').getall()
        for concert_url in yearly_concerts_url:
            yield scrapy.Request(
                url=self.base_url + concert_url,
                method='GET',
                callback=self.parse_concert_article
            )
    
    
    def parse_concert_article(self, response):
        artist_entities_identified = response.xpath('//p/a/text()').getall()
        artist_entities_identified_2 = response.xpath('//table//li/a/text()').getall()

        artist_entities_identified.extend(artist_entities_identified_2)

        artists_tagged = MusicDataScrapersItem()
        
        artists_tagged['url'] = response.request.url
        artists_tagged['artists'] = []
        
        for artist in artist_entities_identified:
            artist_object = self.data_provider.artist_mapper(artist)
            
            if artist_object is not None and artist_object.id not in artists_tagged['artists']:
                artists_tagged['artists'].append(artist_object.id)
        
        yield artists_tagged
        