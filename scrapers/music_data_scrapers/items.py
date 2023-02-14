# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MusicDataScrapersItem(scrapy.Item):
    url = scrapy.Field()
    artists = scrapy.Field()
    
    def __repr__(self):
        return ""
