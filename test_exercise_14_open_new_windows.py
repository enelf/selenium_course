# -*- coding: utf-8 -*-

import unittest
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


ADMIN_PAGE = "http://localhost/litecart/admin/"
COUNTRIES_PAGE = ADMIN_PAGE + "?app=countries&doc=countries"
LOGIN = "admin"
PASSWORD = "admin"


class TestOpenNewWindows(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Firefox()

    def sign_in(self):
        self.driver.get(ADMIN_PAGE)
        self.driver.find_element_by_name("username").send_keys(LOGIN)
        self.driver.find_element_by_name("password").send_keys(PASSWORD)
        self.driver.find_element_by_name("login").click()
        self.driver.maximize_window()

    def test_open_new_windows(self):

        wait = WebDriverWait(self.driver, 5)
        self.sign_in()
        self.driver.get(COUNTRIES_PAGE)

        edit_country_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*=\"app=countries&doc=edit_country\"]")))
        random.choice(edit_country_links).click()
        open_new_window_icons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".fa.fa-external-link")))
        current_window = self.driver.current_window_handle

        for icon in open_new_window_icons:
            opened_windows_before_click = self.driver.window_handles
            icon.click()
            wait.until(lambda driver: len(self.driver.window_handles) > len(opened_windows_before_click))
            opened_windows_after_click = self.driver.window_handles
            assert len(opened_windows_after_click) - len(opened_windows_before_click) == 1
            new_window = list(set(opened_windows_after_click) - set(opened_windows_before_click))[0]
            self.driver.switch_to_window(new_window)
            current_url = self.driver.current_url
            assert ("wikipedia.org" in current_url) or ("www.informatica.com" in current_url)
            self.driver.close()
            self.driver.switch_to_window(current_window)

    def tearDown(self):
        if self.driver:
            self.driver.quit()
