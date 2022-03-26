import time
from threading import Thread

from cointracker.crawler import Crawler
from cointracker.db import InsertFN


class Watcher(Thread):
    def __init__(self, delay: float, crawler: Crawler, insert_fn: InsertFN):
        super().__init__(daemon=True)
        self._delay = delay
        self._crawler = crawler
        self._insert_fn = insert_fn

    def run(self):
        while True:
            self._insert_fn(self._crawler.get_all())
            time.sleep(self._delay)
