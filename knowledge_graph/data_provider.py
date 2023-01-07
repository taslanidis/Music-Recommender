import cdx_toolkit
import threading 
import logging
import gc

from typing import List
from tqdm import tqdm
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
        self._mini_threadpool_executor = ThreadPoolExecutor(max_workers=self._workers//2)
        self._logger = logging.getLogger('ScrapedDataProvider')
        self._cdx = cdx_toolkit.CDXFetcher(source='cc')
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


    def load_data_for_common_crawl_scraper(
        self,
        selected_scraper = CommonCrawlScraper
    ):

        current_scraper = selected_scraper()

        pages = current_scraper.get_pages_from_common_crawl_index(
            threadpool_executor=self._mini_threadpool_executor
        )

        self.process_multiple_pages_in_batches(pages)
    

    def process_multiple_pages_in_batches(
        self, 
        pages: List[cdx_toolkit.CaptureObject],
        selected_scraper: CommonCrawlScraper
    ):

        for i in tqdm(
            iterable=range((len(pages) // (self._batch_size * self._workers)) + int((len(pages) % (self._batch_size * self._workers)) > 0)),
            desc="Batch groups"
        ):

            try:

                futures = []

                for j in range(self._workers):
                    offset = i * (self._batch_size * self._workers) + j * self._batch_size
                    
                    if offset >= len(self._batch_size):
                        break

                    batch_pages = [page for page in pages[offset:offset+self._batch_size]]

                    futures.append(self._threadpool_executor.submit(selected_scraper.parse_pages, batch_pages))

                # wait for all tasks to complete
                wait(futures, return_when=ALL_COMPLETED)

                # clear unused memory from tensorflow trash
                gc.collect()

            except Exception as e:
                self._logger.error(f"Error processing group: {i}. Error details: {e}")
