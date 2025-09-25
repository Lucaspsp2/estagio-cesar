from selenium.webdriver.common.by import By

class Checkboxpage:
    """
    Page Object Model (POM) para a página 'Checkbox' do DemoQA.

    Esta classe encapsula os localizadores (locators) e as ações específicas
    para a interação com o elemento de árvore de checkboxes da página.
    """
    def __init__(self, driver):
        """
        Inicializa o Page Object e define os localizadores da página.

        Args:
            driver: Instância do Selenium WebDriver para interação com o navegador.
        """
        self.driver = driver
        self.url = "https://demoqa.com/checkbox"
        self.expand_all_button = (By.CSS_SELECTOR, "button[title='Expand all']")
        self.label_notes = (By.XPATH, "//label[@for='tree-node-notes']")
        self.notes_input = (By.ID, "tree-node-notes")

    def navigate(self):
        """
        Navega o navegador para a URL da página de Checkbox.
        """

        self.driver.get(self.url)

    def click_expand_all(self):
        """
        Clica no botão 'Expand all' para expandir todos os nós da árvore de checkboxes.
        """
        expand = self.driver.find_element(*self.expand_all_button)
        expand.click()

    def click_label_notes(self):
        """
        Clica no label associado ao checkbox 'Notes' para selecioná-lo/desselecioná-lo.
        """
        self.driver.find_element(*self.label_notes).click()

    def check_notes_is_selected(self):
        """
        Verifica o estado atual de seleção do elemento 'Notes'.

        Retorna:
            bool: True se o checkbox 'Notes' estiver selecionado, False caso contrário.
        """
        return self.driver.find_element(*self.notes_input).is_selected()