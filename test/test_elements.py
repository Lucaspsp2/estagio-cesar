from selenium.webdriver.common.by import By
import time
from pages.elements_pages import ElementsPage
import pytest

@pytest.mark.smoke
@pytest.mark.regression
def test_navigate_to_elements_page(driver):
    elements_page = ElementsPage(driver)
    elements_page.navigate()
    assert "elements" in driver.current_url

@pytest.mark.smoke
def test_locate_by_id(driver):
    elements_page = ElementsPage(driver)
    elements_page.navigate()
    assert elements_page.is_check_box_id_visible()
    assert elements_page.get_menu_check_box_id_text() == "Text Box"

def test_locate_by_css_selector(driver):
    elements_page = ElementsPage(driver)
    elements_page.navigate()
    assert elements_page.is_check_box_css_visible()

@pytest.mark.regression
def test_locate_by_xpath(driver):
    elements_page = ElementsPage(driver)
    elements_page.navigate()
    assert elements_page.is_check_box_xpath_visible()









