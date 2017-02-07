# -*- coding: utf-8 -*-

import unittest
import string
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


MAIN_PAGE = "http://localhost/litecart/"
PASSWORD = "123456"


def get_random_text():
    return "".join([random.choice(string.lowercase) for _ in xrange(random.randint(5, 15))])


def get_random_name():
    return "%s%s" % (random.choice(string.uppercase), get_random_text())


def get_random_email():
    return "%s_%s@example.com" % (get_random_text(), random.randint(111111, 999999))


def get_random_address():
    return "%s str. %s-%s" % (get_random_name(), random.randint(1, 100), random.randint(1, 100))


def get_random_postcode():
    return random.randint(11111, 99999)


def get_random_phone():
    return "+1%s" % random.randint(1111111111, 9999999999)


class TestCreateAccount(unittest.TestCase):
    driver = None

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_create_account(self):

        wait = WebDriverWait(self.driver, 5)
        self.driver.get(MAIN_PAGE)
        self.driver.maximize_window()
        create_account_link = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "a[href*=\"create_account\"")
        ))
        create_account_link.click()

        wait.until(EC.presence_of_element_located((By.NAME, "firstname"))).send_keys(get_random_name())
        self.driver.find_element_by_name("lastname").send_keys(get_random_name())
        self.driver.find_element_by_name("address1").send_keys(get_random_address())
        self.driver.find_element_by_name("postcode").send_keys(get_random_postcode())
        self.driver.find_element_by_name("city").send_keys(get_random_name())
        self.driver.find_element_by_class_name("select2").click()
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".select2-search__field")
        )).send_keys("United States")
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".select2-results li[id*=\"US\"]")
        )).click()
        country_codes = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "(.//select[@name=\"zone_code\"]/option)[position() > 1]")
        ))
        random.choice(country_codes).click()
        user_email = get_random_email()
        self.driver.find_element_by_name("email").send_keys(user_email)
        self.driver.find_element_by_name("phone").send_keys(get_random_phone())
        self.driver.find_element_by_name("password").send_keys(PASSWORD)
        self.driver.find_element_by_name("confirmed_password").send_keys(PASSWORD)
        self.driver.find_element_by_name("create_account").click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*=\"logout\"]"))).click()
        wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(user_email)
        self.driver.find_element_by_name("password").send_keys(PASSWORD)
        self.driver.find_element_by_name("login").click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*=\"logout\"]"))).click()

    def tearDown(self):
        if self.driver:
            self.driver.quit()
