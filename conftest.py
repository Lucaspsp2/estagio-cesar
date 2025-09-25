from selenium import webdriver
import pytest
import json
import time
from pathlib import Path
import os, pytest_html

def pytest_addoption(parser):
    """
    Registra opções de linha de comando personalizadas para o pytest.

    Este hook é invocado pelo pytest durante sua inicialização (geralmente
    no arquivo conftest.py) e permite estender a funcionalidade da CLI.

    As opções adicionadas aqui podem ser acessadas posteriormente nos testes
    ou fixtures através do objeto 'request.config.getoption(...)'.

    Args:
        parser: O objeto `Parser` (semelhante ao argparse) ao qual as
                novas opções de linha de comando devem ser adicionadas.

    Exemplo de uso:
        # Adiciona a flag --browser
        parser.addoption(
            "--browser", action="store", default="chrome", help="Navegador a ser usado nos testes (e.g., chrome ou firefox)"
        )
    """
    parser.addoption("--browser", action="store", default="chrome", help="browser to execute tests (chrome or firefox)")
@pytest.fixture
def driver(request):
    """
    Fixture que inicializa e gerencia o Selenium WebDriver.

    O navegador a ser utilizado é determinado pela opção '--browser'
    passada na linha de comando. A janela é maximizada, e após a
    execução do teste (yield), o navegador é encerrado (quit).

    Args:
        request: Objeto de Request do pytest, usado para acessar opções da CLI.

    Yields:
        webdriver.Chrome ou webdriver.Firefox: A instância do WebDriver configurada.

    Raises:
        ValueError: Se a opção de navegador fornecida não for suportada.
    """
    browser = request.config.getoption("--browser").lower()
    if browser == "chrome":
        driver_instance = webdriver.Chrome()
    elif browser == "firefox":
        driver_instance = webdriver.Firefox()
    else:
        raise ValueError(f"Browser '{browser}' is not supported.")
    driver_instance.maximize_window()
    yield driver_instance
    driver_instance.quit()
    # Fixture to load test data from JSON
# @pytest.fixture(scope="session")
# def test_data():
#     with open("data/test_data.json") as f:
#         return json.load(f)
LOG_FILE = Path("test_durations.log")
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """
    Hook invocado ANTES da execução de cada teste (fase 'setup').

    Registra o tempo de início do teste e o salva no objeto 'item'
    e no arquivo de log.

    Args:
        item: Objeto de item de teste (contém metadados sobre o teste).
    """
    item.start_time = time.time()
    item.start_str = time.strftime("%H:%M:%S", time.localtime())
    msg = f"\n[START] Test '{item.nodeid}' - {item.start_str}"
    print(msg)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(msg + "\n")
@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item):
     """
    Hook invocado APÓS a execução de cada teste (fase 'teardown').

    Calcula a duração total do teste (end_time - start_time) e registra
    o resultado no console e no arquivo de log.

    Args:
        item: Objeto de item de teste (contém o 'start_time' registrado).
    """
     duration = time.time() - item.start_time
     msg = f"[END] Test '{item.nodeid}' finished in {duration:.2f} seconds."
     print(msg)
    # salva em arquivo
     with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(msg + "\n")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook wrapper para processar os resultados da execução do teste.

    É usado para customizar o relatório de testes, especificamente para
    capturar uma screenshot e anexá-la ao relatório HTML se o teste falhar
    durante a fase principal ('call').

    Args:
        item: Objeto de item de teste.
        call: Objeto CallInfo contendo o resultado da execução.

    Yields:
        Outcome: O resultado da chamada para processamento.
    """
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call" and report.failed:
        # Create screenshots directory if it doesn't exist
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        # Take screenshot
        driver = item.funcargs['driver']
        screenshot_file = os.path.join("screenshots", f"{item.name}_error.png")
        driver.save_screenshot(screenshot_file)
        # Add screenshot to the HTML report
        if screenshot_file:
            html = f'<div><img src="{screenshot_file}" alt="screenshot" style="width:304px;height:228px;" ' \
           f'onclick="window.open(this.src)" align="right"/></div>'
            extra.append(pytest_html.extras.html(html))
    report.extra = extra

