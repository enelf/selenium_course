# -*- coding: utf-8 -*-

import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


STORE_PAGE = "http://localhost/litecart/"


class TestCheckStickers(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_check_all_stickers(self):

        wait = WebDriverWait(self.driver, 5)

        self.driver.get(STORE_PAGE)
        products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product")))

        for product in products:
            stickers = product.find_elements_by_css_selector(".sticker")
            self.assertEqual(len(stickers), 1)

    def tearDown(self):
        if self.driver:
            self.driver.quit()
