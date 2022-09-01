# This is a sample Python script.
import json
from multiprocessing import Process, Queue
from typing import List, Tuple

import cloudscraper
from cloudscraper import CloudScraper

from src.dbconnector.dBConnector import SQLiteConnector
from src.page.handlers import ListingPageHandler, ProductPageHandler


def worker_get_details(q):
    productPageHandler: ProductPageHandler = ProductPageHandler()
    sqlite_handler_details: SQLiteConnector = SQLiteConnector()
    while True:
        print(__name__)
        url = q.get()
        print(f'Working on {url}')
        print(url)
        query_url = 'https://batdongsan.com.vn' + url
        details_data = productPageHandler.set_page(query_url).get_items()
        sqlite_handler_details.insert_each_bds_data_details(url, json.dumps(details_data,ensure_ascii=False))
        print(f'Finished {query_url}')


if __name__ == '__main__':
    url_queues = Queue()
    procs_list = []
    for i in range(50):
        procs_list.append(Process(target=worker_get_details, args=(url_queues,)))
    for proccess in procs_list:
        proccess.start()
    scraper: CloudScraper = cloudscraper.create_scraper()
    listenPageHandler: ListingPageHandler = ListingPageHandler()
    sqlite_handler_page: SQLiteConnector = SQLiteConnector()
    # randomlist: object = random.sample(range(20, 500), 20)
    for page in range(1, 788):
        print(page)
        crawled_page: str = 'https://batdongsan.com.vn/ban-can-ho-chung-cu-tp-hcm/p{page}?sortValue=1'.format(page=page)
        print(crawled_page)
        result_list: List[Tuple] = listenPageHandler.set_page(crawled_page).get_items()
        for product in result_list:
            # put the url into the queue
            url_queues.put(product[-1])

        sqlite_handler_page.insert_many_bds_data(result_list)
    for process in procs_list:
        process.join()

        #Handle connection error
