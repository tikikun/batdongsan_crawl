# This is a sample Python script.
import json
import time
import uuid
from multiprocessing import Process, Queue
from typing import List, Tuple

from src.dbconnector.dBConnector import SQLiteConnector
from src.page.handlers import ListingPageHandler, ProductPageHandler


def worker_get_details(q, task_name):
    productPageHandler: ProductPageHandler = ProductPageHandler()
    sqlite_handler_details: SQLiteConnector = SQLiteConnector()
    while True:
        print(__name__)
        queue_dat = q.get()
        url = queue_dat[0]
        queue_id = queue_dat[1]
        print(f'Working on {url}')
        print(url)
        query_url = 'https://batdongsan.com.vn' + url
        details_data = productPageHandler.set_page(query_url).get_items()
        sqlite_handler_details.insert_each_bds_data_details(url, json.dumps(details_data, ensure_ascii=False))
        print(f'Finished {query_url}')
        sqlite_handler_details.remove_queue(task_name, queue_id)


def main(latest_list: List):
    # boilerplate for the task
    task_name = 'query_bds_task'
    crawled_page: str = 'https://batdongsan.com.vn/ban-can-ho-chung-cu-tp-hcm/p{page}?sortValue=1'
    print('this is the latest list',latest_list)
    # start details getting proccesses
    procceses = 8
    url_queues = Queue()
    procs_list = []
    for i in range(8):
        procs_list.append(Process(target=worker_get_details, args=(url_queues, task_name)))
    for proccess in procs_list:
        proccess.start()

    # setup scraper and handler for main proccess
    listenPageHandler: ListingPageHandler = ListingPageHandler()
    sqlite_handler_page: SQLiteConnector = SQLiteConnector()

    # get max page
    max_page: int = listenPageHandler.set_page(crawled_page.format(page='1')).get_max_page()
    print(max_page, 'this is the max page')

    # check if the task is already specified if not create the task with the beginning
    if len(sqlite_handler_page.get_task(task_name)) == 0:
        # set the init task
        print("found no task, we will init a running task")
        sqlite_handler_page.insert_task(task_name, 'running', 0)  # zero because there was no page crawled

    # fetch the task detail after init, or if page len != 0 -> fetch the current task details
    task_details = sqlite_handler_page.get_task(task_name)[0]
    task_name: str = task_details[0]
    task_status: str = task_details[1]
    task_page: int = task_details[2]

    if task_status == 'running':
        # put pending queue into current queue
        queue_items = sqlite_handler_page.get_queue(task_name)
        counter = 0
        for name, url, queue_id in queue_items:
            url_queues.put((url, queue_id))
            print('put item into queue', url, queue_id)
            print(counter)
            counter += 1

        page = task_page
        while page <= max_page:
            # because the task page is already crawled therefore we need to turn next page first
            page += 1
            if page > max_page:
                print('turn to non exist page break here')
                break
            print(page)
            crawled_page = crawled_page.format(page=page)
            print(crawled_page)
            result_list: List[Tuple] = listenPageHandler.set_page(crawled_page).get_items()
            saw_repeated_url = False
            for product in result_list:
                queue_id = str(uuid.uuid1())
                queue_url = product[-1]
                print('this is url for queue test',queue_url)
                if queue_url in latest_list:
                    saw_repeated_url = True
                # put to the database
                sqlite_handler_page.insert_queue(task_name, queue_url, queue_id)
                # put to the url into the queue
                url_queues.put((queue_url, queue_id))
            if saw_repeated_url:
                print('saw repeated url, probably on retry we set status to finished')
                sqlite_handler_page.update_task(task_name,'finished',max_page)
                break
            sqlite_handler_page.update_task(task_name, 'running', page)
            sqlite_handler_page.insert_many_bds_data(result_list)

        print('program end?')
        # end the program and specified ending status
        while len(sqlite_handler_page.get_queue(task_name)) > 0:
            print('wait to finish all the pending tasks for workers')
            time.sleep(1)
        for process in procs_list:
            print(' close proccess:', process)
            process.terminate()
        print('is it really the end?')
        # finshed the job after join on the sub proccess and write record
        sqlite_handler_page.update_task(task_name, 'finished', page)
    elif task_status == 'finished':
        print(task_status, 'because the task is done we will get latest url list')
        sqlite_handler_page.update_task(task_name,'running',0)
        return main(sqlite_handler_page.get_top_latest_20_urls())
    else:
        raise Exception('task status is not found ')

    sqlite_handler_page.update_task(task_name, 'finished', page)


if __name__ == '__main__':
    main([])
