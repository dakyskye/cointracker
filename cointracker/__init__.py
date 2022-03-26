import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from cointracker import db

from cointracker.crawler import BitcoinCrawler
from cointracker.watcher import Watcher


def main():
    tries = 10
    for i in range(tries):
        try:
            db.init()
        except Exception as e:
            if i == tries - 1:
                print(f"database connection attempt failed {tries} times", flush=True)
                return str(e)
        time.sleep(1)

    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument("headless")
    options.add_argument("no-sandbox")
    options.add_argument("dns-prefetch-disable")
    driver = webdriver.Chrome(options=options)

    c = BitcoinCrawler(driver)

    w = Watcher(30, c, db.insert_bitcoin_stat)
    w.start()

    try:
        while w.is_alive():
            pass
    finally:
        db.close()
        driver.quit()
