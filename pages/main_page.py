# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


from .base_page import BasePage


class MainPageLocators(object):
    PRODUCTS = (By.CSS_SELECTOR, ".product.column")


class MainPage(BasePage, MainPageLocators):
    url = "http://localhost/litecart/"

    @property
    def first_product(self):
        products = self.wait.until(
            EC.presence_of_all_elements_located(self.PRODUCTS)
        )
        return products[0]
