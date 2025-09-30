from selenium.webdriver.common.by import By #Definir os localizadores como o By.ID, By.XPATH
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException

class AlertsPage:
    """
    Page Object Model para a página de Alertas, cobrindo a navegação 
    a partir da homepage e a interação com os 4 tipos de alertas.
    """

    # --- LOCALIZADORES ---
    
    # 1. Homepage
    HOMEPAGE_TILE = (By.XPATH, "//h5[text()='Alerts, Frame & Windows']")
    # 2. Alerts, Frame & Windows Page (Sub-menu
    ALERTS_MENU_ITEM = (By.XPATH, "//span[text()='Alerts']")
     
    # 3. Botões de Alerta na página Alerts
    ALERT_BUTTON = (By.ID, "alertButton")
    TIMER_ALERT_BUTTON = (By.ID, "timerAlertButton")
    CONFIRM_BUTTON = (By.ID, "confirmButton")
    PROMPT_BUTTON = (By.ID, "promtButton")
    
    # 4. Resultados de Confirmação/Prompt
    CONFIRM_RESULT = (By.ID, "confirmResult")
    PROMPT_RESULT = (By.ID, "promptResult")

    def __init__(self, driver):
        self.driver = driver

    # --- MÉTODOS DE NAVEGAÇÃO ---

    def navigate_to_alerts_page(self):
        """Navega da Homepage até a sub-página de Alertas."""
        self.driver.get("https://demoqa.com/")
        
        # 1. Clica no tile "Alerts, Frame & Windows" na homepage
        self.driver.find_element(*self.HOMEPAGE_TILE).click()
        
        # 2. Clica no item "Alerts" no sub-menu
        self.driver.find_element(*self.ALERTS_MENU_ITEM).click()

    # --- MÉTODOS DE INTERAÇÃO COM ALERTS (4 MÉTODOS SOLICITADOS) ---

    def handle_simple_alert(self):
        """Clica no botão, aceita o alerta simples e retorna o texto."""
        self.driver.find_element(*self.ALERT_BUTTON).click()
        
        # Aguarda o alerta aparecer
        alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()
        return alert_text

    def handle_delayed_alert(self):
        """Clica no botão, espera 5 segundos, aceita o alerta e retorna o texto."""
        self.driver.find_element(*self.TIMER_ALERT_BUTTON).click()
        
        # Aguarda até que o alerta esteja presente (pode levar até 5 segundos)
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()
        return alert_text

    def handle_confirm_alert(self, accept=False):
        """Clica no botão de confirmação e aceita (True) ou cancela (False) o alerta."""
        self.driver.find_element(*self.CONFIRM_BUTTON).click()
        
        # Aguarda e manipula o alerta
        alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        if accept:
            alert.accept()  # Clica em OK
        else:
            alert.dismiss() # Clica em Cancelar
            
        # Retorna o texto de resultado exibido na tela após a ação
        return self.driver.find_element(*self.CONFIRM_RESULT).text

    def handle_prompt_alert(self, input_text):
        """Clica no prompt, insere um texto, aceita e retorna o texto de resultado."""
        self.driver.find_element(*self.PROMPT_BUTTON).click()
        
        # Aguarda e manipula o alerta
        alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert.send_keys(input_text)
        alert.accept()
        
        # Retorna o texto de resultado exibido na tela, contendo o input
        return self.driver.find_element(*self.PROMPT_RESULT).text
