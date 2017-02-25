# -*- coding: utf-8 -*-

from selenium.webdriver.support.wait import WebDriverWait


TIMEOUT = 3


class BasePage(object):
    url = None

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, TIMEOUT)

    def open(self):
        self.driver.get(self.url)
