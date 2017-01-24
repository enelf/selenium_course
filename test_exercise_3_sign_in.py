# -*- coding: utf-8 -*-

import unittest

from selenium import webdriver


SIGN_IN_PAGE = "http://localhost/litecart/admin/"
LOGIN = "admin"
PASSWORD = "admin"


class TestSignIn(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_sign_in_by_admin(self):
        self.driver.get(SIGN_IN_PAGE)
        self.driver.find_element_by_name("username").send_keys(LOGIN)
        self.driver.find_element_by_name("password").send_keys(PASSWORD)
        self.driver.find_element_by_name("login").click()

    def tearDown(self):
        if self.driver:
            self.driver.quit()
