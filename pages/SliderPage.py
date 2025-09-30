from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class SliderPage:
    """
    Page Object Model para a interação com o elemento Slider, usando ActionChains.
    Implementa JavaScript click para contornar o ElementClickInterceptedException.
    """

    def __init__(self, driver):
        self.driver = driver

    # --- LOCALIZADORES ---
    
    # Navegação: Três passos para chegar no Slider
    # O Tile é o que está na Home Page
    HOMEPAGE_TILE = (By.XPATH, "//h5[text()='Widgets']") 
    
    # O item 'Widgets' no menu lateral (já expandido ou precisa expandir)
    WIDGETS_MENU_ITEM = (By.XPATH, "//div[text()='Widgets']")
    
    # O item 'Slider' no submenu de Widgets
    SLIDER_MENU_ITEM = (By.XPATH, "//span[text()='Slider']")
    
    # Elementos do Slider
    SLIDER_HANDLE = (By.XPATH, "//input[@type='range']")
    VALUE_INPUT = (By.ID, "sliderValue")

    # --- MÉTODOS AUXILIARES ---

    def _js_click(self, locator):
        """Usa JavaScript para forçar o clique, contornando a intercepção de elementos."""
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].click();", element)

    # --- MÉTODOS DE NAVEGAÇÃO ---

    def navigate_to_slider_page(self):
        """Navega da Home Page até a sub-página de Slider."""
        self.driver.get("https://demoqa.com/")
        
        # Clicamos no Tile "Widgets" usando JS Click para evitar intercepção
        self._js_click(self.HOMEPAGE_TILE)
        
        # Clicamos no item "Slider" no menu lateral
        # Não precisamos clicar em 'Widgets' se já clicamos no Tile principal.
        # Aqui, apenas garantimos que o submenu 'Slider' seja clicado.
        self._js_click(self.SLIDER_MENU_ITEM)

        
    # --- MÉTODOS DE INTERAÇÃO COM SLIDER ---
    
    def move_slider_by_keys(self, direction, times):
        # 1. Encontra o elemento do slider
        slider_handle = self.driver.find_element(*self.SLIDER_HANDLE)
        
        # 2. Determina a tecla (Seta Direita ou Seta Esquerda)
        key = Keys.RIGHT if direction == "right" else Keys.LEFT
        
        # 3. Executa o movimento N vezes (o loop)
        for _ in range(times):
            slider_handle.send_keys(key)

    def get_current_value(self):
        """Retorna o valor numérico atual do slider (lido do campo de input)"""
        return self.driver.find_element(*self.VALUE_INPUT).get_attribute("value")
