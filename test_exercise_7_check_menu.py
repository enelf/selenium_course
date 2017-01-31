# -*- coding: utf-8 -*-

import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


SIGN_IN_PAGE = "http://localhost/litecart/admin/"
LOGIN = "admin"
PASSWORD = "admin"


class TestCheckAdminPages(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_check_all_admin_pages(self):

        wait = WebDriverWait(self.driver, 5)

        self.driver.get(SIGN_IN_PAGE)
        self.driver.find_element_by_name("username").send_keys(LOGIN)
        self.driver.find_element_by_name("password").send_keys(PASSWORD)
        self.driver.find_element_by_name("login").click()

        first_menu_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#app->a")))
        first_menu_links = [x.get_attribute("href") for x in first_menu_elements]

        for link in first_menu_links:
            self.driver.get(link)
            first_menu_item_header = self.driver.find_elements_by_css_selector("#content>h1")
            self.assertTrue(first_menu_item_header)

            second_menu_elements = self.driver.find_elements_by_css_selector(".docs a")
            second_menu_links = [x.get_attribute("href") for x in second_menu_elements]

            if second_menu_elements:
                for link in second_menu_links:
                    self.driver.get(link)
                    second_menu_item_header = self.driver.find_elements_by_css_selector("#content>h1")
                    self.assertTrue(second_menu_item_header)

    def tearDown(self):
        if self.driver:
            self.driver.quit()
