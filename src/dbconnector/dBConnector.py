from typing import List, Tuple, Any

import jaydebeapi
from jaydebeapi import Cursor


class SQLiteConnector:
    def __init__(self):
        self.database = "/Users/daotuan/PycharmProjects/pythonProject/bds_db.db"

        self.conn = jaydebeapi.connect("org.sqlite.JDBC",
                                       f"""jdbc:sqlite:{self.database}""",
                                       None,
                                       '/Users/daotuan/PycharmProjects/pythonProject/sqlite-jdbc-3.39.2.1.jar')

    def insert_each_bds_data(self, title: str, price: str, price_per_m2: str, area: str, date: str, url: str):
        curs: Cursor = self.conn.cursor()
        print("INSERT INTO bds_data values('{}','{}','{}','{}','{}');".format(title, price, price_per_m2, area, date))
        curs.execute('INSERT INTO bds_data values(?,?,?,?,?);', (title, price, price_per_m2, area, date))
        curs.close()

    def insert_many_bds_data(self, result_list: List[Tuple]):
        curs: Cursor = self.conn.cursor()
        curs.executemany('INSERT INTO bds_data values(?,?,?,?,?,?)', result_list)
        curs.close()

    def get_all_bds_data(self):
        curs: Cursor = self.conn.cursor()
        curs.execute('select * from bds_data')
        result: List[Tuple[Any, ...]] = curs.fetchall()
        return result
