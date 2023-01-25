import logging

from typing import Dict, List, Optional
from tqdm import tqdm
from datetime import datetime, timedelta
from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, wait


class DeafultScraper:
    pass


class WikipediaScraper(DeafultScraper):

    def __init__(self):
        self.source = "en.wikipedia.org/wiki/*"
        self._logger = logging.getLogger('WikipediaScraper')

    
class RedditScraper(DeafultScraper):

    def __init__(self):
        self._logger = logging.getLogger('RedditScraper')


class BillboardScraper(DeafultScraper):

    def __init__(self):
        self.source = "billboard.com/c/music/*"
        self._logger = logging.getLogger('BillboardScraper')