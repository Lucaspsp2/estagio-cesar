from selenium.webdriver.common.by import By
import time

def test_check_box(driver):
    driver.get("https://demoqa.com/checkbox")
    
    # Expand the tree
    expand_all_button = driver.find_element(By.CSS_SELECTOR, "button[title='Expand all']")
    expand_all_button.click()
    
    # Select the checkbox "Notes"
    notes_checkbox = driver.find_element(By.XPATH, "//label[@for='tree-node-notes']")
    notes_checkbox.click()
    
    # Validate if checkbox was ticked
    notes_input = driver.find_element(By.ID, "tree-node-notes")
    assert notes_input.is_selected()

def test_check_box_commands(driver):
    driver.get("https://demoqa.com/checkbox")

    expand_all_button = driver.find_element(By.CSS_SELECTOR, "button[title='Expand all']")
    expand_all_button.click()
    
    # Select the checkbox "Notes"
    notes_checkbox = driver.find_element(By.XPATH, "//label[@for='tree-node-commands']")
    notes_checkbox.click()
    
    
    # Validate if checkbox was ticked
    notes_input = driver.find_element(By.ID, "tree-node-commands")
    assert notes_input.is_selected()
    
