from pages.AlertsPage import AlertsPage
from selenium.webdriver.common.by import By
import time # Importar time para fins de visualização do teste

# A fixture 'driver' é injetada automaticamente pelo conftest.py em cada teste.

def navigate_and_get_page_object(driver):
    """
    Navega para a página de Alertas a partir da Home Page (se necessário) 
    e retorna a instância do Page Object.
    """
    alerts_page = AlertsPage(driver)
    
    # Navega para a página de Alertas, se já não estiver nela, 
    # evitando navegação repetida em todos os 4 testes.
    if not "alerts" in driver.current_url:
        alerts_page.navigate_to_alerts_page()
    
    # Pequena espera para garantir que a página carregue completamente
    time.sleep(0.5) 
    return alerts_page

def test_01_simple_alert(driver):
    """Testa a interação com o 'Click button to see alert'."""
    print("\n--- Teste 1: Alerta Simples ---")
    alerts_page = navigate_and_get_page_object(driver)
    
    alert_text = alerts_page.handle_simple_alert()
    assert alert_text == "You clicked a button"
    print(f"Alerta Simples: '{alert_text}' aceito com sucesso.")


def test_02_delayed_alert(driver):
    """Testa a interação com o 'On button click, alert will appear after 5 seconds'."""
    print("\n--- Teste 2: Alerta Atrasado (5s) ---")
    alerts_page = navigate_and_get_page_object(driver)
    
    # Este teste é mais lento, pois espera 5 segundos
    delayed_alert_text = alerts_page.handle_delayed_alert()
    assert delayed_alert_text == "This alert appeared after 5 seconds"
    print(f"Alerta Atrasado: '{delayed_alert_text}' aceito com sucesso.")


def test_03_confirm_alert(driver):
    """Testa a interação com o 'On button click, confirm box will appear' (Cancelando)."""
    print("\n--- Teste 3: Alerta de Confirmação ---")
    alerts_page = navigate_and_get_page_object(driver)
    
    # Clica no botão e escolhe 'Cancelar' (accept=False)
    confirm_result_cancel = alerts_page.handle_confirm_alert(accept=False)
    assert "Cancel" in confirm_result_cancel
    print(f"Confirmação: Resultado esperado 'Cancel' obtido: {confirm_result_cancel}")


def test_04_prompt_alert(driver):
    """Testa a interação com o 'On button click, prompt box will appear' (Inserindo texto)."""
    print("\n--- Teste 4: Alerta de Prompt ---")
    alerts_page = navigate_and_get_page_object(driver)
    
    input_value = "Quatro Alertas"
    # Clica no botão, insere o texto e clica em 'OK'
    prompt_result = alerts_page.handle_prompt_alert(input_value)
    # Note que usamos 'in' porque o resultado completo é 'You entered Quatro Alertas'
    assert f"You entered {input_value}" in prompt_result 
    print(f"Prompt: Resultado esperado 'You entered {input_value}' obtido: {prompt_result}")