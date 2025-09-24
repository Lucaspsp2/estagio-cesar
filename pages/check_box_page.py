from selenium.webdriver.common.by import By

class Checkboxpage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://demoqa.com/checkbox"
        self.expand_all_button = (By.CSS_SELECTOR, "button[title='Expand all']")
        self.label_notes = (By.XPATH, "//label[@for='tree-node-notes']")
        self.notes_input = (By.ID, "tree-node-notes")

    def navigate(self):
        self.driver.get(self.url)

    def click_expand_all(self):
        expand = self.driver.find_element(*self.expand_all_button)
        expand.click()

    def click_label_notes(self):
        self.driver.find_element(*self.label_notes).click()

    def check_notes_is_selected(self):
        return self.driver.find_element(*self.notes_input).is_selected()