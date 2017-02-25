# -*- coding: utf-8 -*-

import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from .base_page import BasePage


class ProductPageLocators(object):
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "button[value=\"Add To Cart\"]")
    SIZE_OPTIONS = (
        By.XPATH, "(.//select[@name=\"options[Size]\"]/option)[position() > 1]"
    )
    ITEMS_QUANTITY = (By.CSS_SELECTOR, "#cart .quantity")
    CHECKOUT_LINK = (By.CSS_SELECTOR, "a[href*=\"checkout\"]:nth-of-type(3)")


class ProductPage(BasePage, ProductPageLocators):

    @property
    def add_to_cart_btn(self):
        return self.wait.until(
            EC.presence_of_element_located(self.ADD_TO_CART_BTN)
        )

    @property
    def size_options(self):
        try:
            return self.wait.until(EC.presence_of_all_elements_located(
                self.SIZE_OPTIONS
            ))
        except TimeoutException:
            return []

    def get_items_quantity(self):
        return int(self.wait.until(
            EC.presence_of_element_located(self.ITEMS_QUANTITY)
        ).text)

    def select_random_size_option_if_drop_down_is_present(self):
        size_options = self.size_options
        if size_options:
            random.choice(size_options[1:]).click()

    def add_product_to_cart(self):
        before_add_item_quantity = self.get_items_quantity()
        self.select_random_size_option_if_drop_down_is_present()
        self.add_to_cart_btn.click()
        self.wait.until(
            lambda driver: int(self.wait.until(EC.presence_of_element_located(
                self.ITEMS_QUANTITY
            )).text) > before_add_item_quantity)

    def checkout(self):
        self.wait.until(
            EC.presence_of_element_located(self.CHECKOUT_LINK)
        ).click()
