from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PracticeFormPage:
    ''' Page Object para a página 'Student Registration Form' do DemoQA.

    Esta classe implementa o padrão Page Object Model (POM) para
    abstrair a interação com os elementos da página do formulário
    de registro de estudantes, contendo todos os localizadores
    e métodos de interação.'''
    def __init__(self, driver):
        """
        Inicializa o Page Object e define os localizadores da página.

        Args:
            driver: Instância do WebDriver (e.g., Chrome, Firefox) para
                    interagir com a página.
        """
        self.driver = driver
        self.url = "https://demoqa.com/automation-practice-form"
        self.first_name_input = (By.ID, "firstName")
        self.last_name_input = (By.ID, "lastName")
        self.email_input = (By.ID, "userEmail")
        self.gender_radio = (By.XPATH, "//label[text()='{}']")
        self.mobile_input = (By.ID, "userNumber")
        self.dob_input = (By.ID, "dateOfBirthInput")
        self.subjects_input = (By.ID, "subjectsInput")
        self.hobbies_checkbox = (By.XPATH, "//label[text()='{}']")
        self.picture_upload = (By.ID, "uploadPicture")
        self.address_textarea = (By.ID, "currentAddress")
        self.state_dropdown = (By.ID, "state")
        self.city_dropdown = (By.ID, "city")
        self.submit_button = (By.ID, "submit")
        self.out_put_modal = (By.ID, "example-modal-sizes-title-lg")
        self.subjects_input = (By.ID, "subjectsInput")
        self.subjects_text = (By.ID, "react-select-2-option-0") # novo locator para o click do subject  
    
    def navigate(self):
         """Navega o navegador para a URL da página do formulário."""
         self.driver.get(self.url)

    def fill_form(self, data):
        """
        Preenche o formulário de registro de estudantes com dados fornecidos.

        Args:
            data (dict): Dicionário contendo todos os dados a serem inseridos
                         no formulário. Deve incluir chaves como 'first_name',
                         'gender', 'subjects', 'state', etc.
        """
        self.driver.find_element(*self.first_name_input).send_keys(data["first_name"])
        self.driver.find_element(*self.last_name_input).send_keys(data["last_name"])
        self.driver.find_element(*self.email_input).send_keys(data["email"])
        self.driver.find_element(By.XPATH, f"//label[text()='{data['gender']}']").click()
        self.driver.find_element(*self.mobile_input).send_keys(data["mobile"])
        
        # Date of Birth
        dob_field = self.driver.find_element(*self.dob_input)
        dob_field.send_keys(Keys.CONTROL + "a")
        dob_field.send_keys(data["dob"])
        dob_field.send_keys(Keys.ENTER)

        # Subjects
        subjects_field = self.driver.find_element(*self.subjects_input)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", subjects_field)
        for subject in data["subjects"]:
            subjects_field.send_keys(subject)
            subjects_text = self.wait.until(
                EC.element_to_be_clickable(self.subjects_text)
           )
        subjects_text.click()

        # Hobbies
        for hobby in data["hobbies"]:
            self.driver.find_element(By.XPATH, f"//label[text()='{hobby}']").click()

        # Picture
        # self.driver.find_element(*self.picture_upload).send_keys(data["picture"])

        self.driver.find_element(*self.address_textarea).send_keys(data["address"])
        
        # State and City
        state_element = self.driver.find_element(*self.state_dropdown)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", state_element)

        self.driver.find_element(*self.state_dropdown).click()
        self.driver.find_element(By.XPATH, f"//*[text()='{data['state']}']").click()
        
        self.driver.find_element(*self.city_dropdown).click()
        self.driver.find_element(By.XPATH, f"//*[text()='{data['city']}']").click()


    def submit_form(self):
        """
        Submete o formulário, acionando o botão 'Submit'.
        
        Realiza um scroll até o botão antes de clicar.
        """
        button = self.driver.find_element(*self.submit_button)
        self.driver.find_element(*self.submit_button).click()
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)

    def check_modal_visible(self):
        """
        Verifica se o modal de confirmação de envio do formulário está visível.

        Returns:
            bool: True se o modal estiver visível, False caso contrário.
        """
        return self.driver.find_element(*self.out_put_modal).is_displayed()