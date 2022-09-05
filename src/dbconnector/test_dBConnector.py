from unittest import TestCase

from src.dbconnector.dBConnector import SQLiteConnector


class TestSQLiteConnector(TestCase):
    def test_get_task(self):
        print(SQLiteConnector().get_task("alan"))

    def test_insert_task(self):
        SQLiteConnector().insert_task("alan", "failed", 100)

    def test_update_tasl(self):
        SQLiteConnector().update_task('alan', 'hahaha', '200')
        print(SQLiteConnector().get_task('alan'))

    def test_not_found(self):
        assert len(SQLiteConnector().get_task('thang nao')) == 0
