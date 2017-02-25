# -*- coding: utf-8 -*-

import unittest

from selenium import webdriver
from pages.main_page import MainPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


NUMBER_OF_PRODUCTS = 3


class TestAddCartItems(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()

    def test_add_cart_items(self):

        main_page = MainPage(self.driver)
        product_page = None

        for _ in xrange(NUMBER_OF_PRODUCTS):
            main_page.open()
            main_page.first_product.click()
            product_page = ProductPage(self.driver)
            product_page.add_product_to_cart()

        product_page.checkout()
        cart_page = CartPage(self.driver)
        cart_page.wait_for_confirm_btn_present()
        cart_page.remove_all_items()
        cart_page.wait_for_confirm_btn_disappear()
        self.assertEqual(
            cart_page.get_checkout_text_present(),
            "There are no items in your cart."
        )

    def tearDown(self):
        if self.driver:
            self.driver.quit()
