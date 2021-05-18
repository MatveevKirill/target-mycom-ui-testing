import time
import logging

import allure
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ActionChains, Chrome
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import exceptions

from common import exceptions as CE
from utils.decorators import wait

COUNT_CLICK_RETRY = 3


class BasePageActions(object):
    url = None
    locators = None

    def __init__(self, driver: Chrome, configuration: dict, is_opened_params: dict = None) -> None:
        """
        Инициализация базового класса для работы с элементами на странице.
        :param driver: драйвер Google Chrome.
        :param configuration: конфигурация тестирования.
        :param is_opened_params: параметры для проверки текущей страницы драйвера и url PageObject.
        """
        self.driver = driver
        self.configuration = configuration
        assert self._is_opened(is_opened_params)

    def go_to(self, page_name: str = "dashboard", **kwargs):
        """
        Переход на другую страницу.
        Примечание: т.к. страница Кампании вызывается непосредственно на странице Dashboard, то в классе наследнике
        присутствуют дополнительно методы go_to_create_campaign и go_to_campaign.
        :param page_name: название страницы.
        :param kwargs: дополнительные параметры при инициализации классов наследников.
        :return: DashboardPage or SegmentsPage.
        """
        from ui.pages.dashboard_page import DashboardPage
        from ui.pages.segments_page import SegmentsPage

        if page_name == "dashboard":
            self.click(
                locator=(
                    self.locators.BUTTON_NAVIGATION_TEMPLATE[0],
                    self.locators.BUTTON_NAVIGATION_TEMPLATE[1].format("Кампании")
                )
            )
            dashboard = DashboardPage(driver=self.driver, configuration=self.configuration, **kwargs)
            self.write_log(f"Going from: '{self.__class__.__name__}' to '{dashboard.__class__.__name__}'.")
            return dashboard
        elif page_name == "segments":
            self.click(
                locator=(
                    self.locators.BUTTON_NAVIGATION_TEMPLATE[0],
                    self.locators.BUTTON_NAVIGATION_TEMPLATE[1].format("Аудитории")
                )
            )
            segments = SegmentsPage(driver=self.driver, configuration=self.configuration, **kwargs)
            self.write_log(f"Going from: '{self.__class__.__name__}' to '{segments.__class__.__name__}'.")
            return segments
        else:
            raise CE.NotFindPageObject(f"Not find page '{page_name}'.")

    def _is_opened(self, is_opened_params: dict = None) -> bool:
        """
        Проверка на то, что страница загрузилась.
        :param is_opened_params: параметры для проверки страницы.
        :return: bool.
        """

        def _check_url(params: dict =None) -> bool:
            """
            Проверка url драйвера и url PageObject`а.
            :param is_opened_params: параметры для проверки URL.
            :return: Bool.
            """
            if params is None:
                params = {
                    "ignore_get_params": False,
                    "new_url": None
                }

            current_url = self.driver.current_url.split("#")[0]

            if 'new_url' in params and params['new_url']:
                url = params['new_url']
            else:
                url = self.driver.current_url.split("#")[0]

            if 'ignore_get_params' in params and params['ignore_get_params']:
                current_url = current_url.split("?")[0]
                url = url.split("?")[0]

            if current_url != url:
                raise CE.PageNotLoadedException(
                    f"Page not loaded (current_url='{current_url}';url='{url}')"
                )
            return True

        return wait(
            _method=_check_url,
            _error=CE.PageNotLoadedException,
            _check=True,
            params=is_opened_params
        )

    @allure.step("Click on locator: {locator}")
    def click(self, locator: tuple) -> None:
        """
        Нажать на элемент на странице.
        :param locator: локатор элемента.
        :return: None.
        """
        def _click():
            self.action_chains.click(on_element=self.find_element(locator=locator)).perform()
            return

        return wait(
            _method=_click,
            _error=exceptions.StaleElementReferenceException,
            _timeout=self.configuration['timeout_limit']
        )

    def send_keys(self, locator: tuple = None, send_data: str = "", auto_clear: bool = True) -> None:
        """
        Отправить данные через ActionChains.send_keys.
        :param locator: локатор элемента.
        :param send_data: отправляемые данные.
        :param auto_clear: автоматическая очистка элемента перед отправкой. По умолчанию: True.
        :return: None
        """
        def _send_keys():
            element = self.find_element(locator=locator)
            if auto_clear:
                element.clear()
            return self.action_chains.send_keys_to_element(element, send_data).perform()

        return wait(
            _method=_send_keys,
            _error=exceptions.TimeoutException,
            _timeout=self.configuration['timeout_limit']
        )

    def scroll_to(self, locator: tuple = None) -> None:
        """
        Переместиться к элементу на странице.
        :param locator: локатор элемента.
        :return: None
        """
        def _scroll_to():
            return self.action_chains.move_to_element(
                to_element=(self.wait().until(EC.visibility_of_element_located(locator=locator)))
            )

        return wait(
            _method=_scroll_to,
            _error=exceptions.TimeoutException,
            _timeout=self.configuration['timeout_limit']
        )

    def wait(self, timeout: float = None) -> WebDriverWait:
        """
        Настройка ожиданий.
        :param timeout: время ожидания. По умолчанию: None.
        :return: WebDriverWait.
        """
        if timeout is None:
            timeout = self.configuration['timeout_limit']
        return WebDriverWait(self.driver, timeout=timeout)

    def find_element(self, locator: tuple, timeout: float = None) -> WebElement:
        """
        Найти элемент на странице.
        :param locator: локатор элемента.
        :param timeout: время для нахождения элемента.
        :return: WebElement
        """
        return self.wait(timeout=timeout).until(EC.presence_of_element_located(locator=locator))

    def get_text_from_element(self, locator: tuple, timeout: float = None) -> str:
        """
        Получение текста из элемента страницы.
        :param locator: локатор элемента.
        :param timeout: время для нахождения элемента.
        :return: str
        """
        def _get() -> str:
            return self.find_element(locator=locator, timeout=timeout).text

        return wait(
            _method=_get,
            _error=exceptions.StaleElementReferenceException,
            _timeout=self.configuration['timeout_limit']
        )

    def get_attr_from_element(self, attribute_name: str, locator: tuple, timeout: float = None) -> str:
        """
            Получение атрибута из элемента.
            :param attribute_name: название атрибута.
            :param locator: локатор элемента.
            :param timeout: время для нахождения элемента.
            :return: str
        """
        def _get():
            return self.find_element(locator=locator, timeout=timeout).get_attribute(attribute_name)

        return wait(
            _method=_get,
            _error=exceptions.StaleElementReferenceException,
            _timeout=self.configuration['timeout_limit']
        )

    def get_selected_from_element(self, locator: tuple, timeout: float = None) -> str:
        """
        Получение значения True|False из is_selected элемента.
        :param locator: локатор элемента.
        :param timeout: время для нахождения элемента.
        :return: bool.
        """
        def _get():
            return self.find_element(locator=locator, timeout=timeout).is_selected()

        return wait(
            _method=_get,
            _error=exceptions.StaleElementReferenceException,
            _timeout=self.configuration['timeout_limit']
        )

    def refresh(self) -> None:
        """
        Обновить текущую страницу.
        :return: None
        """
        self.driver.refresh()

    def switch_tab(self, tab_id: int, close_prev: bool = False) -> None:
        """
        Сменить активное окно.
        :param tab_id: Идентификатор окна.
        :param close_prev: необходимо ли закрывать предыдущее окно.
        :return: None.
        """
        if close_prev:
            if len(self.driver.window_handles) < 2:
                raise CE.CannotCloseWindowException(
                    "it is impossible to close the window if there are less than 2 of them")
            self.driver.close()
            tab_id -= 1
        self.driver.switch_to.window(self.driver.window_handles[tab_id])

    def write_log(self, log: str, level: str = "info") -> None:
        """
        Запись в лог файл.
        :param log: лог.
        :param level: уровень лога.
        :return: None
        """
        logger = logging.getLogger('pytest-logger')

        if level == "info":
            logger.info(log)
        elif level == "debug":
            logger.debug(log)
        elif level == "warning":
            logger.warning(log)
        elif level == "error":
            logger.error(log)
        else:
            raise CE.IncorrectLoggerType(f"Incorrect logger type. Get type '{level}'.")

    @property
    def action_chains(self) -> ActionChains:
        """
        Вернуть объект Action Chains в Selenium.
        :return: ActionChains property.
        """
        return ActionChains(self.driver)
