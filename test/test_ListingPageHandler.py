import unittest
from unittest import TestCase
from ..src.page.ListingPageHandler import ListingPageHandler


class TestListingPageHandler(TestCase):
    edge_case: str = 'https://batdongsan.com.vn/ban-can-ho-chung-cu/p3?sortValue=1'
    non_edge_case: str = 'https://batdongsan.com.vn/ban-can-ho-chung-cu-can-ho-hoang-quoc-viet?sortValue=1'

    def test_get_items(self):
        pageHandler: ListingPageHandler = ListingPageHandler()
        pageHandler.set_page(self.non_edge_case)
        try:
            res: list = pageHandler.get_items()
            self.assertGreater(len(res), 0)
            print(res)
        except IndexError:
            self.fail("Index error exception")

    def test_get_items_edge_case(self):
        pageHandler: ListingPageHandler = ListingPageHandler()
        pageHandler.set_page(self.edge_case)
        try:
            res: list = pageHandler.get_items()
            self.assertGreater(len(res), 0)
            print(res)
        except IndexError:
            self.fail("Index error exception")




if __name__ == '__main__':
    unittest.main()
