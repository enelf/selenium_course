# -*- coding: utf-8 -*-

import pytest
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


PATH_TO_GECKO = "C:\geckodriver.exe"
PATH_TO_FIREFOX = "C:\Program Files\Mozilla Firefox 47\\firefox.exe"


@pytest.fixture
def driver(request):
    wd = webdriver.Firefox(
        executable_path=PATH_TO_GECKO,
        firefox_binary=FirefoxBinary(firefox_path=PATH_TO_FIREFOX)
    )
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    driver.get("http://www.google.com/")
    driver.find_element_by_name("q").send_keys("webdriver")
    driver.find_element_by_name("btnG").click()
    WebDriverWait(driver, 10).until(EC.title_is(u"webdriver - Пошук Google"))
