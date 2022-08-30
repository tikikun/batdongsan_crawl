import time
from typing import List, Tuple

import cloudscraper
from bs4 import BeautifulSoup, Tag
from cloudscraper import CloudScraper
from requests import Response


class ListingPageHandler:
    def __init__(self):
        self.page = None

    def set_page(self, page):
        self.page = page
        return self

    def get_items(self) -> List:
        result = self.__get_items_data_pretty()
        if result == [] or result is None:
            return self.get_items()
        return result


    def __get_items_data_pretty(self) -> List[Tuple]:
        scraper: CloudScraper = cloudscraper.create_scraper()
        result: List[Tuple] = []
        scraper: CloudScraper = scraper
        data: Response = scraper.get(self.page)
        data.encoding = 'utf-8'
        print(data.status_code)
        soup: BeautifulSoup = BeautifulSoup(data.text, 'html.parser')

        # print(soup.prettify())
        info_cards = soup.select('#product-lists-web > div > a > div.re__card-info')
        for card in info_cards:
            # All cases will have these
            title: str = card.select(".re__card-title")[0].text.strip()
            spans: Tag = card.select(".re__card-config")[0]
            date: str = card.select('.re__card-contact')[0].select('.re__card-published-info-published-at')[0].attrs[
                'aria-label']
            # Check case
            try:
                price: str = spans.select('.re__card-config-price')[0].text
            except IndexError:
                price: str = None
            try:
                price_per_m2: str = spans.select('.re__card-config-price_per_m2')[0].text
            except IndexError:
                price_per_m2: str = None
            try:
                area: str = spans.select('.re__card-config-area')[0].text
            except IndexError:
                area: str = None
            result.append((title, price, price_per_m2, area, date))
        return result
