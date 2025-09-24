from selenium.webdriver.common.by import By

class ElementsPage:
    def __int__(self, driver):
        self.driver = driver
        self.url = "https://demoqa.com/elements"
        self.menu_check_box_id = (By.ID, "Item-0")
        self.menu_check_box_css = (By.CSS_SELECTOR, "Item-0")
        self.menu_check_box_xpath = (By.XPATH, "//span[text()='Text Box']")



    def navigate(self):
        self.driver.get(self.url)
    
    def is_check_box_id_visible(self):
        return self.driver.find_element(*self.menu_check_box_id).is_displayed()
    
    def get_new_check_box_id_text(self):
        return self.driver.find_element(*self.menu_check_box_id).text
    
    def is_check_box_css_visible(self):
        return self.driver.find_element(*self.menu_check_box_css).is_displayed()
    
    def is_check_box_xpath_visible(self):
        return self.driver.find_element(*self.menu_check_box_xpath).is_displayed()
    
    

    