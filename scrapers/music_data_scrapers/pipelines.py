# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json


class MusicDataScrapersPipeline:
    
    def open_spider(self, spider):
        self.records = []


    def close_spider(self, spider):
        with open(f'./dataset/{spider.name}_artists_graph.json', 'w') as outfile:
            json.dump(self.records, outfile, indent=4)
        
    
    def process_item(self, item, spider):
        self.records.append({"url": item['url'], "artists": item['artists']})
