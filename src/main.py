# This is a sample Python script.
import random
import jaydebeapi
import cloudscraper
from cloudscraper import CloudScraper
from src.page.ListingPageHandler import ListingPageHandler

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to/ search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scraper: CloudScraper = cloudscraper.create_scraper()
    listenPageHandler: ListingPageHandler = ListingPageHandler()
    randomlist = random.sample(range(20, 500), 20)
    for page in randomlist:
        print('https://batdongsan.com.vn/ban-can-ho-chung-cu-tp-hcm/p{page}?sortValue=1'.format(page=page))
        print(page, listenPageHandler.set_page(
            'https://batdongsan.com.vn/ban-can-ho-chung-cu-tp-hcm/p{page}?sortValue=1'.format(page=page)).get_items())
