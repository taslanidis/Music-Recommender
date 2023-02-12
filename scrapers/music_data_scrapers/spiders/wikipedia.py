import scrapy

from recommender_system.data_engineering.data_provider import DataProvider


class Wikipedia(scrapy.Spider):
    name = "wikipedia"
    allowed_domains = [
        'wikipedia.com'
    ]
    wikipedia_root_pages = [
        "https://en.wikipedia.org/wiki/List_of_music_genres_and_styles",
        "https://en.wikipedia.org/wiki/List_of_electronic_music_genres",
        "https://en.wikipedia.org/wiki/Lists_of_musicians"
    ]
    data_provider = DataProvider()


    def start_requests(self):
        for url in self.wikipedia_root_pages:
            yield scrapy.Request(url=url,method='GET')


    def parse(self, response):
        music_genres_url = response.xpath('//li/a/@href').all()
        for genre_url in music_genres_url:
            yield scrapy.Request(
                url=genre_url,
                method='GET',
                callback=self.parse_genre_article
            )
    
    
    def parse_genre_article(self, response):
        artist_entities_identified = response.xpath('//p/a/text()').all()
        artists_tagged = []
        for artist in artist_entities_identified:
            artist_id = self.data_provider.get_artist_by_name(artist)
            artists_tagged.append(artist_id)
        # TODO: save item with URL -> list of artists mentioned
        