from unittest import TestCase
from src.page.handlers import ListingPageHandler

class TestListingPageHandler(TestCase):
    def test_get_max_page(self):
        print( ListingPageHandler().set_page('https://batdongsan.com.vn/ban-can-ho-chung-cu-tp-hcm').get_max_page() )
