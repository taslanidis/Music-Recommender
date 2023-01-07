import scrapy


class Songkick(scrapy.Spider):
    name = "ap-news"
    allowed_domains = [
        'songkick.com'
    ]
    news_urls = [
        "https://www.songkick.com/leaderboards/popular_artists",
        "https://www.songkick.com/leaderboards/popular_artists?page=2",
        "https://www.songkick.com/leaderboards/popular_artists?page=3",
        "https://www.songkick.com/leaderboards/popular_artists?page=4",
        "https://www.songkick.com/leaderboards/popular_artists?page=5"
    ]


    def start_requests(self):
        for url in self.news_urls:
            yield scrapy.Request(url=url,method='GET')


    def parse(self, response):
        articles = response.xpath('//div[contains(@class, "FeedCard") and @data-tb-region-item]')