from typing import List, Tuple, Dict

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
        product_lists = soup.select('#product-lists-web > div')
        for product in product_lists:
            info_card = product.select('a > div.re__card-info')[0]
            # getting url
            url: str = product.select('a')[0].attrs['href']
            # info card All cases will have these
            title: str = info_card.select(".re__card-title")[0].text.strip()
            spans: Tag = info_card.select(".re__card-config")[0]
            date: str = \
                info_card.select('.re__card-contact')[0].select('.re__card-published-info-published-at')[0].attrs[
                    'aria-label']
            # Check case
            try:
                price: str = spans.select('.re__card-config-price')[0].text
            except IndexError:
                price = None
            try:
                price_per_m2: str = spans.select('.re__card-config-price_per_m2')[0].text
            except IndexError:
                price_per_m2 = None
            try:
                area: str = spans.select('.re__card-config-area')[0].text
            except IndexError:
                area = None
            result.append((title, price, price_per_m2, area, date, url))
        return result

    def get_max_page(self) -> int:
        result = self.__get_max_page()
        if result is None:
            return self.get_max_page()
        return result

    def __get_max_page(self) -> int:
        scraper: CloudScraper = cloudscraper.create_scraper()
        scraper: CloudScraper = scraper
        data: Response = scraper.get(self.page)
        data.encoding = 'utf-8'
        print(data.status_code)
        soup: BeautifulSoup = BeautifulSoup(data.text, 'html.parser')
        try:
            total_page: int = int(soup.select('#listing-page-info')[0].attrs['data-total-page'])
        except IndexError:
            return None
        return total_page


class ProductPageHandler:
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

    def __get_items_data_pretty(self) -> Dict:
        scraper: CloudScraper = cloudscraper.create_scraper()
        result: List[Tuple] = []
        scraper: CloudScraper = scraper
        data: Response = scraper.get(self.page)
        data.encoding = 'utf-8'
        print(data.status_code)
        soup: BeautifulSoup = BeautifulSoup(data.text, 'html.parser')
        try:
            product_details = soup.select(
                "#product-detail-web > div.re__section.re__pr-specs.re__pr-specs-v1.js__section > div > div")[0]
        except IndexError:
            return []
        item_titles = product_details.select('.re__pr-specs-content-item-title')
        item_values = product_details.select('.re__pr-specs-content-item-value')
        result = {}
        for title, value in zip(item_titles, item_values):
            result[title.text] = value.text
        return result


if __name__ == '__main__':
    prodhandler = ProductPageHandler()
    page = 'https://batdongsan.com.vn/ban-condotel-xa-bao-ninh-prj-dolce-penisola-quang-binh/ban-can-codoltel-view-bien-gia-1-2-ty-1-can-thanh-toan-tu-3-5-pr34662414'
    prodhandler.set_page(page)
    product_details = prodhandler.get_items()
    print(product_details)
