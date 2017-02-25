# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage


class CartPageLocators(object):
    CONFIRM_ORDER_BTN = (By.CSS_SELECTOR, '[name="confirm_order"]')
    SHORTCUTS = (By.CSS_SELECTOR, ".shortcut")
    REMOVE_BTN = (By.CSS_SELECTOR, "[name=\"remove_cart_item\"]")
    CHECKOUT_WRAPPER = (By.CSS_SELECTOR, "#checkout-cart-wrapper em")


class CartPage(BasePage, CartPageLocators):

    def wait_for_confirm_btn_present(self):
        self.confirm_btn = self.wait.until(
            EC.presence_of_element_located(self.CONFIRM_ORDER_BTN)
        )

    @property
    def shortcuts(self):
        return self.wait.until(
            EC.presence_of_all_elements_located(self.SHORTCUTS)
        )

    @property
    def remove_btn(self):
        return self.wait.until(EC.presence_of_element_located(self.REMOVE_BTN))

    def remove_item(self):
        remove_btn = self.remove_btn
        remove_btn.click()
        self.wait.until(EC.staleness_of(remove_btn))

    def remove_all_items(self):
        shortcuts = self.shortcuts
        if shortcuts:
            for _ in xrange(len(shortcuts)):
                self.remove_item()
        else:
            self.remove_btn.click()

    def wait_for_confirm_btn_disappear(self):
        self.wait.until(EC.staleness_of(self.confirm_btn))

    def get_checkout_text_present(self):
        return self.wait.until(
            EC.presence_of_element_located(self.CHECKOUT_WRAPPER)
        ).text
