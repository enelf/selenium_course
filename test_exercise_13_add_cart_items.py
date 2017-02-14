# -*- coding: utf-8 -*-

import unittest
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


STORE_PAGE = "http://localhost/litecart/"
NUMBER_OF_PRODUCTS = 3


class TestAddCartItems(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()

    def test_add_cart_items(self):

        wait = WebDriverWait(self.driver, 5)

        for _ in xrange(NUMBER_OF_PRODUCTS):
            self.driver.get(STORE_PAGE)
            products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product.column")))
            products[0].click()
            add_to_cart_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[value=\"Add To Cart\"]")))
            size_options = self.driver.find_elements_by_xpath("(.//select[@name=\"options[Size]\"]/option)[position() > 1]")
            if size_options:
                random.choice(size_options[1:]).click()

            before_add_item_quantity = int(self.driver.find_element_by_css_selector("#cart .quantity").text)
            add_to_cart_btn.click()
            wait.until(lambda driver: int(self.driver.find_element_by_css_selector("#cart .quantity").text) > before_add_item_quantity)

        self.driver.find_element_by_css_selector("a[href*=\"checkout\"]:nth-of-type(3)").click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[name=\"confirm_order\"]")))

        shortcuts = self.driver.find_elements_by_css_selector(".shortcut")
        if shortcuts:
            for _ in xrange(len(shortcuts)):
                remove_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[name=\"remove_cart_item\"]")))
                remove_btn.click()
                wait.until(EC.staleness_of(remove_btn))
        else:
            self.driver.find_element_by_css_selector("[name=\"remove_cart_item\"]").click()

        checkout_wrapper = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#checkout-cart-wrapper em")))
        assert checkout_wrapper.text == "There are no items in your cart."

    def tearDown(self):
        if self.driver:
            self.driver.quit()
