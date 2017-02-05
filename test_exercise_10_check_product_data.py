# -*- coding: utf-8 -*-

import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


STORE_PAGE = "http://localhost/litecart/"
EXPECTED_REGULAR_PRICE_COLOR = ["rgb(119, 119, 119)", "rgba(119, 119, 119, 1)"]
EXPECTED_REGULAR_PRICE_TEXT_STYLE = "line-through"
EXPECTED_CAMPAIGN_PRICE_COLOR = ["rgb(204, 0, 0)", "rgba(204, 0, 0, 1)"]
EXPECTED_CAMPAIGN_PRICE_TAG = "STRONG"
EXPECTED_PRODUCT_CARD_REGULAR_PRICE_COLOR = ["rgb(102, 102, 102)", "rgba(102, 102, 102, 1)"]


@pytest.fixture(
    params=[webdriver.Chrome, webdriver.Firefox, webdriver.Ie, webdriver.Edge],
    ids=["Chrome", "Firefox", "Ie", "Edge"]
)
def driver(request):
    browser = request.param()
    request.addfinalizer(browser.quit)
    return browser


def get_font_size_and_convert_to_float(element):
    return float(element.value_of_css_property("font-size").replace("px", ""))


def test_check_product_data(driver):

    driver = driver

    wait = WebDriverWait(driver, 5)
    driver.get(STORE_PAGE)
    driver.maximize_window()

    product = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#box-campaigns .product.column")))
    product_name = product.find_element_by_css_selector(".name").text
    regular_price_element = product.find_element_by_css_selector(".regular-price")
    campaign_price_element = product.find_element_by_css_selector(".campaign-price")
    regular_price = regular_price_element.text
    campaign_price = campaign_price_element.text
    regular_price_color = regular_price_element.value_of_css_property("color")
    assert regular_price_color in EXPECTED_REGULAR_PRICE_COLOR
    campaign_price_color = campaign_price_element.value_of_css_property("color")
    assert campaign_price_color in EXPECTED_CAMPAIGN_PRICE_COLOR
    regular_price_text_style = regular_price_element.value_of_css_property("text-decoration")
    assert regular_price_text_style == EXPECTED_REGULAR_PRICE_TEXT_STYLE
    campaign_price_text_style = campaign_price_element.get_attribute("tagName")
    assert campaign_price_text_style == EXPECTED_CAMPAIGN_PRICE_TAG
    regular_price_text_size = get_font_size_and_convert_to_float(regular_price_element)
    campaign_price_text_size = get_font_size_and_convert_to_float(campaign_price_element)
    assert campaign_price_text_size > regular_price_text_size

    driver.get(product.find_element_by_css_selector("a").get_attribute("href"))

    product_card = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#box-product")))
    product_card_name = product_card.find_element_by_css_selector(".title").text
    assert product_name == product_card_name
    product_card_regular_price = product_card.find_element_by_css_selector(".regular-price")
    assert regular_price == product_card_regular_price.text
    product_card_campaign_price = product_card.find_element_by_css_selector(".campaign-price")
    assert campaign_price == product_card_campaign_price.text
    product_card_regular_price_color = product_card_regular_price.value_of_css_property("color")
    assert product_card_regular_price_color in EXPECTED_PRODUCT_CARD_REGULAR_PRICE_COLOR
    product_card_campaign_price_color = product_card_campaign_price.value_of_css_property("color")
    assert product_card_campaign_price_color in EXPECTED_CAMPAIGN_PRICE_COLOR
    product_card_regular_price_text_style = product_card_regular_price.value_of_css_property("text-decoration")
    assert product_card_regular_price_text_style == EXPECTED_REGULAR_PRICE_TEXT_STYLE
    product_card_campaign_price_text_style = product_card_campaign_price.get_attribute("tagName")
    assert product_card_campaign_price_text_style == EXPECTED_CAMPAIGN_PRICE_TAG
    product_card_regular_price_text_size = get_font_size_and_convert_to_float(product_card_regular_price)
    product_card_campaign_price_text_size = get_font_size_and_convert_to_float(product_card_campaign_price)
    assert product_card_campaign_price_text_size > product_card_regular_price_text_size
