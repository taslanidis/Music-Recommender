import threading 
import logging
import gc

from typing import List
from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, wait

from settings import Settings
from knowledge_graph.scrapers import (
    DeafultScraper, 
    CommonCrawlScraper,
    WikipediaScraper, 
    RedditScraper, 
    BillboardScraper
)


class ScrapedDataProvider:

    def __init__(self):
        self._write_lock = threading.Lock()
        self._workers = 16
        self._threadpool_executor = ThreadPoolExecutor(max_workers=self._workers)
        self._logger = logging.getLogger('ScrapedDataProvider')
        self._scrapers = [
            WikipediaScraper,
            RedditScraper,
            BillboardScraper
        ]
        self._batch_size = 100

    
    def load_data_for_api_scraper(
        self,
        selected_scraper = DeafultScraper
    ):

        current_scraper = selected_scraper()
        
        # TODO: execute
