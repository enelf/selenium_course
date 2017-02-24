# -*- coding: utf-8 -*-

import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


ADMIN_PAGE = "http://localhost/litecart/admin/"
CATALOG_PAGE = ADMIN_PAGE + "?app=catalog&doc=catalog&category_id=1"
LOGIN = "admin"
PASSWORD = "admin"


class TestCheckConsoleLogs(unittest.TestCase):
    driver = None

    def setUp(self):
        capabilities = DesiredCapabilities.CHROME
        capabilities['loggingPrefs'] = {'browser': 'ALL'}
        self.driver = webdriver.Chrome(desired_capabilities=capabilities)

    def sign_in(self):
        self.driver.get(ADMIN_PAGE)
        self.driver.find_element_by_name("username").send_keys(LOGIN)
        self.driver.find_element_by_name("password").send_keys(PASSWORD)
        self.driver.find_element_by_name("login").click()
        self.driver.maximize_window()

    def test_check_console_logs(self):

        wait = WebDriverWait(self.driver, 5)
        self.sign_in()
        self.driver.get(CATALOG_PAGE)
        edit_links = [x.get_attribute("href") for x in wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '[name="catalog_form"] a[href*="?app=catalog&doc=edit_product"]:nth-child(2)')
        ))]

        all_console_logs = []

        for link in edit_links:
            self.driver.get(link)
            browser_logs = self.driver.get_log("browser")
            if browser_logs:
                all_console_logs.append((self.driver.current_url, browser_logs))

        self.assertFalse(all_console_logs)

    def tearDown(self):
        if self.driver:
            self.driver.quit()
