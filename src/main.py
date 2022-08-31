# This is a sample Python script.
import random
from typing import List, Tuple

import jaydebeapi
import cloudscraper
from cloudscraper import CloudScraper
from src.page.handlers import ListingPageHandler
from src.dbconnector.dBConnector import SQLiteConnector

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to/ search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scraper: CloudScraper = cloudscraper.create_scraper()
    listenPageHandler: ListingPageHandler = ListingPageHandler()
    sqlite_handler: SQLiteConnector =  SQLiteConnector()
    # randomlist: object = random.sample(range(20, 500), 20)
    for page in range(1,788):
        print(page)
        crawled_page: str = 'https://batdongsan.com.vn/ban-can-ho-chung-cu-tp-hcm/p{page}?sortValue=1'.format(page=page)
        print(crawled_page)
        result_list: List[Tuple] = listenPageHandler.set_page(crawled_page).get_items()
        print(result_list)
        sqlite_handler.insert_many_bds_data(result_list)
