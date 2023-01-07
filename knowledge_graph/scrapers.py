import logging
import cdx_toolkit

from typing import Dict, List, Optional
from tqdm import tqdm
from datetime import datetime, timedelta
from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, wait


class DeafultScraper:
    
    pass


class CommonCrawlScraper:

    _logger: logging.Logger
    _cdx: cdx_toolkit.CDXFetcher
    _source: str

    def get_pages_from_common_crawl_index(
        self, 
        threadpool_executor: ThreadPoolExecutor
    ) -> List[cdx_toolkit.CaptureObject]:
        
        batch_interval = timedelta(days=90)
        current_dt = datetime.today()
        futures = []
        
        while current_dt > datetime.today() - timedelta(days=365):

            from_ts = (current_dt - batch_interval).strftime("%Y%m")
            to = current_dt.strftime("%Y%m")
            current_dt -= batch_interval
            
            future = threadpool_executor.submit(
                self.search_in_common_crawl_index,
                from_ts,
                to
            )

            futures.append(future)

        # wait for all tasks to complete
        wait(futures, return_when=ALL_COMPLETED)

        result = []
        for future in futures:
            future_result = future.result()
            
            if future_result is not None:
                result.extend(future_result)

        return result


    def search_in_common_crawl_index(
        self, 
        from_ts: str, 
        to: str
    ) -> List[cdx_toolkit.CaptureObject]:
        self._logger.info(f"Searching in CC Index <source={self._source}, fromts={from_ts}, to:{to}>")
        return list(self._cdx.iter(self._source, from_ts=from_ts, to=to, filter='=status:200'))


    def decide_which_pages_to_download(
        self, 
        pages: List[cdx_toolkit.CaptureObject]
    ) -> List[int]:

        # TODO
        pass


    def parse_pages(
        self, 
        pages: List[cdx_toolkit.CaptureObject]
    ):
        """Splits article processing in batches, executed in multithreading
        """
        pages_indexes_to_download = self.decide_which_pages_to_download(pages)
            
        for page_index in pages_indexes_to_download:
            
            try:
                if pages[page_index] is None:
                    continue

                # TODO: process
            
            except Exception as e:
                self._logger.error(f"{e}")


class WikipediaScraper(CommonCrawlScraper):

    def __init__(self):
        self.source = "en.wikipedia.org/wiki/*"
        self._logger = logging.getLogger('WikipediaScraper')
        self._cdx = cdx_toolkit.CDXFetcher(source='cc')

    
class RedditScraper(DeafultScraper):

    def __init__(self):
        self._logger = logging.getLogger('RedditScraper')


class BillboardScraper(CommonCrawlScraper):

    def __init__(self):
        self.source = "billboard.com/c/music/*"
        self._logger = logging.getLogger('BillboardScraper')
        self._cdx = cdx_toolkit.CDXFetcher(source='cc')