from typing import List, Tuple, Any

import jaydebeapi
from jaydebeapi import Cursor
import pathlib

class SQLiteConnector:
    def __init__(self):
        self.database = "/Users/daotuan/PycharmProjects/pythonProject/bds_db.db"

        self.conn = jaydebeapi.connect("org.sqlite.JDBC",
                                       f"""jdbc:sqlite:{self.database}""",
                                       None,
                                       '/Users/daotuan/PycharmProjects/pythonProject/sqlite-jdbc-3.39.2.1.jar')

    def insert_bds_data(self, title, price, price_per_m2, area, date):
        curs: Cursor = self.conn.cursor()
        curs.execute("INSERT INTO bds_data values('{}','{}','{}','{}','{}')".format(title, price, price_per_m2, area, date))
        curs.close()

    def get_all_bds_data(self):
        curs: Cursor = self.conn.cursor()
        curs.execute('select * from bds_data')
        result: List[Tuple[Any, ...]] = curs.fetchall()
        return result
