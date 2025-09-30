from selenium import webdriver
import pytest
import json
import time
from pathlib import Path
import os, pytest_html
import csv
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

report_data = []

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

def pytest_generate_tests(metafunc):
    if "browser" in metafunc.fixturenames:
        browser = metafunc.config.getoption("browser").split(",")
        metafunc.parametrize("browser", browser)

# @pytest.fixture(params=["chrome", "firefox"], scope="function")
# def driver(browser):
#     if browser == "chrome":
#         options = ChromeOptions()
#     elif browser == "firefox":
#         options = FirefoxOptions()
#     else:
#         raise ValueError(f"Browser not supported: {browser}")

#     driver = webdriver.Remote(
#         command_executor="http://localhost:4444/wd/hub",
#         options=options,
#     )

#     yield driver
#     driver.quit()
@pytest.fixture

@pytest.fixture(params=["chrome", "firefox"], scope="function")
def driver(request):
    # browser = request.config.getoption("--browser").lower()
    browser = request.param
    if browser == "chrome":
        driver_instance = webdriver.Chrome()
    elif browser == "firefox":
        driver_instance = webdriver.Firefox()
    else:
        raise ValueError(f"Browser '{browser}' is not supported.")
    
    driver_instance.maximize_window()
    request.node.browser = browser

    yield driver_instance
    driver_instance.quit()

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
    if report.when == "call": # and report.failed:

        status = 'Passed' if report.passed else 'Failed'
        browser = getattr(item, 'browser', 'N/A')
        test_name = item.name
        duration = f"{report.duration:.4f}s"

        if report.failed:
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
        
        report_data.append({
            "browser": browser.capitalize(),
            "test_case_name": test_name,
            "status": status,
            "timestamp": duration
        })

    report.extra = extra
def pytest_sessionstart(session):
    # Called before tests run
    pass    

def pytest_sessionfinish(session, exitstatus):
    # Called after all tests run
    pass
    """
    Hook executed in the end of test session to create the CSV report.
    """
    if not report_data:
        return
        
    # Ordena os dados por navegador para um relatório mais legível
    sorted_reports = sorted(report_data, key=lambda x: x['browser'])
    
    keys = sorted_reports[0].keys()
    
    with open('test_report.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(sorted_reports)

    print("\nReport 'test_report.csv' generated successfully")

def pytest_collection_modifyitems(session, config, items):
    items.reverse()  # run tests in reverse order
    
def pytest_collection_modifyitems(config, items):
    for item in items:
        if "slow" in item.keywords and not config.getoption("--runslow"):
            item.add_marker(pytest.mark.skip(reason="need --runslow option to run"))



@pytest.fixture(scope="class")
def class_resource():
    print("\n[SETUP] class_resource")
    yield "class fixture"
    print("[TEARDOWN] class_resource")

@pytest.fixture(scope="module")
def module_resource():
    print("\n[SETUP] module_resource")
    yield "module fixture"
    print("[TEARDOWN] module_resource")

@pytest.fixture(scope="session")
def session_resource():
    print("\n[SETUP] session_resource")
    yield "session fixture"
    print("[TEARDOWN] session_resource")
                