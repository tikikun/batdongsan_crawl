from typing import List, Tuple, Any

import jaydebeapi
from jaydebeapi import Cursor


class SQLiteConnector:
    def __init__(self):
        self.database = "bds_db.db"

        self.conn = jaydebeapi.connect("org.sqlite.JDBC",
                                       f"""jdbc:sqlite:{self.database}""",
                                       None,
                                       'sqlite-jdbc-3.39.2.1.jar')

    def insert_each_bds_data(self, title: str, price: str, price_per_m2: str, area: str, date: str, url: str):
        curs: Cursor = self.conn.cursor()
        print("INSERT INTO bds_data values('{}','{}','{}','{}','{}');".format(title, price, price_per_m2, area, date))
        curs.execute('INSERT INTO bds_data values(?,?,?,?,?);', (title, price, price_per_m2, area, date))
        curs.close()

    def insert_each_bds_data_details(self, url: str, details: str):
        curs: Cursor = self.conn.cursor()
        curs.execute('INSERT INTO bds_data_details values(?,?)', (url, details))
        curs.close()

    def insert_many_bds_data(self, result_list: List[Tuple]):
        curs: Cursor = self.conn.cursor()
        curs.executemany('INSERT INTO bds_data values(?,?,?,?,?,?)', result_list)
        curs.close()

    def get_task(self, task_name):
        curs: Cursor = self.conn.cursor()
        curs.execute("SELECT * FROM bds_data_tasks WHERE name = ?", (task_name,))
        result: List[Tuple[Any, ...]] = curs.fetchall()
        curs.close()
        return result

    def insert_task(self, task_name: str, task_status: str, page: int):
        curs: Cursor = self.conn.cursor()
        curs.execute('INSERT INTO bds_data_tasks values(?,?,?)', (task_name, task_status, page))
        curs.close()

    def update_task(self, task_name: str, task_status: str, page: int):
        curs: Cursor = self.conn.cursor()
        curs.execute('UPDATE bds_data_tasks SET status = ?, page = ? WHERE name = ?', (task_status, page, task_name))
        print("Save the process of task", task_name, task_status, page)
        curs.close()

    def insert_queue(self, task_name: str, url: str, queue_id: str):
        curs: Cursor = self.conn.cursor()
        curs.execute('INSERT INTO bds_data_queues values(?,?,?)', (task_name, url, queue_id))
        curs.close()

    def get_queue(self, task_name: str):
        curs: Cursor = self.conn.cursor()
        curs.execute("SELECT * FROM bds_data_queues WHERE task_name = ?", (task_name,))
        result: List[Tuple[Any, ...]] = curs.fetchall()
        curs.close()
        return result

    def remove_queue(self, url: str, queue_id: str):
        curs: Cursor = self.conn.cursor()
        curs.execute('DELETE FROM bds_data_queues WHERE queue_id = ?', (queue_id,))
        print("Delete the item ", queue_id, "with", url, "from the task list")
        curs.close()

    def get_all_bds_data(self):
        curs: Cursor = self.conn.cursor()
        curs.execute('select * from bds_data')
        result: List[Tuple[Any, ...]] = curs.fetchall()
        curs.close()
        return result
