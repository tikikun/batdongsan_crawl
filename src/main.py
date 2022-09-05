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
        sqlite_handler_details.insert_each_bds_data_details(url, json.dumps(details_data, ensure_ascii=False))
        print(f'Finished {query_url}')


if __name__ == '__main__':
    # boilerplate for the task
    task_name = 'query_bds_task'

    # start details getting proccesses
    procceses = 8
    url_queues = Queue()
    procs_list = []
    for i in range(8):
        procs_list.append(Process(target=worker_get_details, args=(url_queues,)))
    for proccess in procs_list:
        proccess.start()

    # setup scraper and handler for main proccess
    scraper: CloudScraper = cloudscraper.create_scraper()
    listenPageHandler: ListingPageHandler = ListingPageHandler()
    sqlite_handler_page: SQLiteConnector = SQLiteConnector()

    # check if the task is already specified if not create the task with the beginning
    if len(sqlite_handler_page.get_task(task_name)) == 0:
        start_page = 0
        # set the init task
        print("found no task, we will init a running task")
        sqlite_handler_page.insert_task(task_name, 'running', 1)

    # fetch the task detail after init, or if page len != 0 -> fetch the current task details
    task_details = sqlite_handler_page.get_task(task_name)[0]
    task_name: str = task_details[0]
    task_status: str = task_details[1]
    task_page: int = task_details[2]

    if task_status == 'running':
        for page in range(task_page, 788):
            print(page)
            crawled_page: str = f'https://batdongsan.com.vn/ban-can-ho-chung-cu-tp-hcm/p{page}?sortValue=1'
            print(crawled_page)
            result_list: List[Tuple] = listenPageHandler.set_page(crawled_page).get_items()
            for product in result_list:
                # put the url into the queue
                url_queues.put(product[-1])
            sqlite_handler_page.update_task(task_name, 'running', page)
            sqlite_handler_page.insert_many_bds_data(result_list)
        # end the program and specified ending status
        for process in procs_list:
            process.join()
    else:
        print('the task is not running, it must be old task or ended task -> you need to build update new task flow ')

    sqlite_handler_page.update_task(task_name, 'finished', page)
