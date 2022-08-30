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


    database = "bds_db.db"

    conn = jaydebeapi.connect("org.sqlite.JDBC",
                              f"""jdbc:sqlite:{database}""",
                              None,
                              'sqlite-jdbc-3.39.2.1.jar')
    curs = conn.cursor()
    curs.execute("select * from bds_data")
    records = curs.fetchall()
    # print(records)
    # scraper: CloudScraper = cloudscraper.create_scraper()
    # listenPageHandler: ListingPageHandler = ListingPageHandler()
    # randomlist = random.sample(range(20, 500), 20)
    # for page in randomlist:
    #     print('https://batdongsan.com.vn/ban-can-ho-chung-cu-tp-hcm/p{page}?sortValue=1'.format(page=page))
    #     print(page, listenPageHandler.set_page(
    #         'https://batdongsan.com.vn/ban-can-ho-chung-cu-tp-hcm/p{page}?sortValue=1'.format(page=page)).get_items())
