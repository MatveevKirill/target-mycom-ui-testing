import os
import pytest
import allure
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from _pytest.fixtures import FixtureRequest

from ui.pages.login_page import LoginPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.campaign_page import CampaignPage
from ui.pages.segments_page import SegmentsPage

from creds import Credentials


@pytest.fixture()
def dashboard(login_page: LoginPage) -> DashboardPage:
    creds = Credentials()
    login_page.login(creds.LOGIN, creds.PASSWORD)
    return DashboardPage(driver=login_page.driver, configuration=login_page.configuration)


@pytest.fixture()
def login_page(driver: webdriver.Chrome, configuration: dict) -> LoginPage:
    return LoginPage(driver=driver, configuration=configuration)


@pytest.fixture()
def dashboard_page(driver: webdriver.Chrome, configuration: dict) -> DashboardPage:
    return DashboardPage(driver=driver, configuration=configuration)


@pytest.fixture()
def campaign_page(driver: webdriver.Chrome, configuration: dict) -> CampaignPage:
    return CampaignPage(driver=driver, configuration=configuration)


@pytest.fixture()
def segments_page(driver: webdriver.Chrome, configuration: dict) -> SegmentsPage:
    return SegmentsPage(driver=driver, configuration=configuration)


@pytest.fixture()
def driver_chrome_options() -> webdriver.ChromeOptions:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("ignore-certificate-errors")
    return chrome_options


@pytest.fixture()
def driver(driver_chrome_options: webdriver.ChromeOptions) -> webdriver.Chrome:
    manager = ChromeDriverManager(version="latest", log_level=0)
    driver = webdriver.Chrome(executable_path=manager.install(), options=driver_chrome_options)
    driver.get("https://target.my.com/")
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope="function", autouse=True)
def ui_report(driver: webdriver.Chrome, request: FixtureRequest, test_dir: str) -> None:
    failed = request.session.testsfailed
    yield
    if request.session.testsfailed > failed:
        screenshot_file = os.path.join(test_dir, 'failure.png')
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'failure.png', attachment_type=allure.attachment_type.PNG)

        browser_logfile = os.path.join(test_dir, 'browser.log')
        with open(browser_logfile, 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")

        with open(browser_logfile, 'r') as f:
            allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)
