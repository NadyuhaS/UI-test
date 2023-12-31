import pytest
import string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='firefox',
                     help="Choose browser: firefox or chrome")


@pytest.fixture(scope="class")
def browser(request):
    options = Options()
    options.headless = True
    if request.config.getoption("browser_name").lower() == 'chrome':
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif request.config.getoption("browser_name").lower() == 'firefox':
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
    yield driver
    driver.quit()