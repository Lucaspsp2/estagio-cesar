from selenium.webdriver.common.by import By
import time
from pages.test_box_page import TextBoxPage

def test_fill_test_box_form_and_validate(driver):
    test_box_page = TextBoxPage(driver)
    test_box_page.load()

    full_name = "Lucas"
    email = "lpsp@cesar.org.br"
    current_address = "Rua da Boa Vista, s/n"
    permanent_address = "Rua do barco, s/n"    

    test_box_page.fill_form(full_name, email, current_address, permanent_address)
    test_box_page.submit_form()

    output = test_box_page.get_output_text()

    assert full_name in output
    assert email in output
    assert current_address in output
    assert permanent_address in output