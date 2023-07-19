import pytest
import string
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose browser: firefox or chrome")


@pytest.fixture(scope="session")
def browser(request):
    if request.config.getoption("browser_name").lower() == 'chrome':
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif request.config.getoption("browser_name").lower() == 'firefox':
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    yield driver
    driver.quit()
