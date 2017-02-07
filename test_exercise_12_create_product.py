# -*- coding: utf-8 -*-

import os
import unittest
import string
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


ADMIN_PAGE = "http://localhost/litecart/admin/"
CATALOG_PAGE = ADMIN_PAGE + "?app=catalog&doc=catalog"
LOGIN = "admin"
PASSWORD = "admin"
PATH_TO_IMG = os.path.normpath(os.path.join(os.getcwd(), "blue-duck.png"))


def get_random_text():
    return "".join([random.choice(string.lowercase) for _ in xrange(random.randint(5, 15))])


def get_random_name():
    return "%s%s Duck" % (random.choice(string.uppercase), get_random_text())


def get_description():
    return (
        "Nulla nec scelerisque felis. Donec dictum lacus non tristique venenatis. "
        "Nulla facilisi. Maecenas at justo aliquam, dignissim tortor id, auctor mauris. "
        "Aliquam at lacinia arcu, laoreet aliquet diam. Sed ac pellentesque tortor, quis maximus leo. "
        "Aenean elit diam, faucibus hendrerit justo tristique, blandit sollicitudin dolor. "
        "Nam risus neque, porta at purus quis, tristique molestie dui. "
        "Sed fringilla neque condimentum, finibus ligula quis, rutrum nibh. "
        "Aenean egestas nisi at ex placerat ullamcorper. Nulla facilisi."
    )

def get_short_description():
    return "Nulla nec scelerisque felis. Donec dictum lacus non tristique venenatis."


def get_random_code():
    return "rd%s" % random.randint(111, 999)


class TestCreateProduct(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Firefox()

    def sign_in(self):
        self.driver.get(ADMIN_PAGE)
        self.driver.find_element_by_name("username").send_keys(LOGIN)
        self.driver.find_element_by_name("password").send_keys(PASSWORD)
        self.driver.find_element_by_name("login").click()
        self.driver.maximize_window()

    def test_create_product(self):

        wait = WebDriverWait(self.driver, 5)
        self.sign_in()
        self.driver.get(CATALOG_PAGE)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "a[href*=\"doc=edit_product\"]")
        )).click()
        random.choice(wait.until(EC.presence_of_all_elements_located((By.NAME, "status")))).click()
        product_name = get_random_name()
        self.driver.find_element_by_name("name[en]").send_keys(product_name)
        self.driver.find_element_by_name("code").send_keys(get_random_code())
        category = random.choice(self.driver.find_elements_by_name("categories[]"))
        if not category.is_selected():
            category.click()
        quantity = self.driver.find_element_by_name("quantity")
        quantity.clear()
        quantity.send_keys(random.randint(1, 100))
        random.choice(self.driver.find_elements_by_xpath(
            "(.//select[@name=\"sold_out_status_id\"]/option)[position() > 1]"
        )).click()
        self.driver.find_element_by_name("new_images[]").send_keys(PATH_TO_IMG)
        self.driver.find_element_by_css_selector("a[href*=\"#tab-information\"]").click()
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[name=\"manufacturer_id\"] option[value=\"1\"]")
        )).click()
        self.driver.find_element_by_name("short_description[en]").send_keys(get_short_description())
        description = self.driver.find_element_by_css_selector(".trumbowyg-editor")
        self.driver.execute_script("arguments[0].textContent=\"%s\"" % get_description(), description)
        self.driver.find_element_by_css_selector("a[href*=\"#tab-prices\"]").click()
        purchase_price = wait.until(EC.presence_of_element_located((By.NAME, "purchase_price")))
        purchase_price.clear()
        purchase_price.send_keys(random.randint(1, 999))
        random.choice(self.driver.find_elements_by_xpath(
            "(.//select[@name=\"purchase_price_currency_code\"]/option)[position() > 1]"
        )).click()
        self.driver.find_element_by_name("prices[USD]").send_keys(random.randint(1, 999))
        self.driver.find_element_by_name("prices[EUR]").send_keys(random.randint(1, 999))
        self.driver.find_element_by_name("save").click()

        wait.until(EC.presence_of_element_located((By.XPATH, ".//a[contains(text(), \"%s\")]" % product_name)))

    def tearDown(self):
        if self.driver:
            self.driver.quit()
