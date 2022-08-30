import unittest
import pathlib
from unittest import TestCase
from ..src.dbconnector.dBConnector import SQLiteConnector


class TestSQLiteConnector(TestCase):
    def test_insert_bds_data(self):
        print(pathlib.Path().resolve())
        print('ahaha')

    def test_get_all_bds_data(self):
        print(SQLiteConnector().get_all_bds_data())

if __name__ == '__main__':
    print(pathlib.Path().resolve())
    unittest.main()
