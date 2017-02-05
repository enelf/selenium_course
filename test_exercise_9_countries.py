# -*- coding: utf-8 -*-

import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


ADMIN_PAGE = "http://localhost/litecart/admin/"
COUNTRIES_PAGE = ADMIN_PAGE + "?app=countries&doc=countries"
GEO_ZONES_PAGE = ADMIN_PAGE + "?app=geo_zones&doc=geo_zones"
LOGIN = "admin"
PASSWORD = "admin"


class TestCheckCountriesAndGeoZones(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Firefox()

    def sign_in(self):
        self.driver.get(ADMIN_PAGE)
        self.driver.find_element_by_name("username").send_keys(LOGIN)
        self.driver.find_element_by_name("password").send_keys(PASSWORD)
        self.driver.find_element_by_name("login").click()
        self.driver.maximize_window()

    def test_check_countries(self):

        wait = WebDriverWait(self.driver, 5)
        self.sign_in()
        self.driver.get(COUNTRIES_PAGE)
        current_countries = []
        not_null_zones_country_links = []
        country_rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".row")))

        for row in country_rows:
            country = row.find_element_by_css_selector("td:nth-child(5) a")
            current_countries.append(country.text)
            zones = row.find_element_by_css_selector("td:nth-child(6)")
            if int(zones.text) > 0:
                not_null_zones_country_links.append(country.get_attribute("href"))

        expected_countries = sorted(current_countries)
        self.assertListEqual(current_countries, expected_countries)

        for link in not_null_zones_country_links:
            self.driver.get(link)
            current_country_zones = [x.text for x in wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, "(.//*[@id=\"table-zones\"]//td[3])[position() < last()]")
            ))]
            expected_country_zones = sorted(current_country_zones)
            self.assertListEqual(current_country_zones, expected_country_zones)

    def test_check_geo_zones(self):

        wait = WebDriverWait(self.driver, 5)
        self.sign_in()
        self.driver.get(GEO_ZONES_PAGE)

        country_edit_links = [x.get_attribute("href") for x in wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".row [title=\"Edit\"]")
        ))]

        for link in country_edit_links:
            self.driver.get(link)
            current_country_zones = [x.text for x in wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "#table-zones td:nth-child(3) option[selected]")
            ))]
            expected_country_zones = sorted(current_country_zones)
            self.assertListEqual(current_country_zones, expected_country_zones)

    def tearDown(self):
        if self.driver:
            self.driver.quit()
