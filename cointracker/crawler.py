from typing import TypedDict

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def _normalise(elem: WebElement):
    return float(elem.text.replace(",", "").removeprefix("$"))


class CrawlerResult(TypedDict):
    price_current: float
    price_24h_low: float
    price_24h_high: float


class Crawler:
    _URL = ""
    _CURRENT_XPATH = ""
    _24H_LOW_XPATH = ""
    _24H_HIGH_XPATH = ""

    def __init__(self, driver: WebDriver):
        self._driver = driver

    def finish(self):
        self._driver.close()

    def _get_current(self):
        return _normalise(self._driver.find_element(by=By.XPATH, value=self._CURRENT_XPATH))

    def _get_24h_low(self):
        return _normalise(self._driver.find_element(by=By.XPATH, value=self._24H_LOW_XPATH))

    def _get_24h_high(self):
        return _normalise(self._driver.find_element(by=By.XPATH, value=self._24H_HIGH_XPATH))

    def get_all(self) -> CrawlerResult:
        self._driver.get(self._URL)
        return {
            'price_current': self._get_current(),
            'price_24h_low': self._get_24h_low(),
            'price_24h_high': self._get_24h_high()
        }


class BitcoinCrawler(Crawler):
    _URL = "https://www.coindesk.com/price/bitcoin/"
    _CURRENT_XPATH = "/html/body/div[1]/div/div[2]/div[2]/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/span[2]"
    _24H_LOW_XPATH = "/html/body/div[1]/div/div[2]/div[2]/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div[2]/div[2]/span"
    _24H_HIGH_XPATH = "/html/body/div[1]/div/div[2]/div[2]/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div[3]/div[2]/span"
