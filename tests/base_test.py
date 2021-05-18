import pytest
import logging
from selenium.webdriver import Chrome


class BaseTestCase(object):
    driver = None
    configuration = None
    logger = None

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, driver: Chrome, configuration: dict, logger: logging.Logger) -> None:
        """
        Установить параметры для тестирования.
        :param driver: драйвер Google Chrome.
        :param configuration: конфигурация тестирования.
        :param logger: логирование.
        :return: None
        """
        self.driver = driver
        self.configuration = configuration
        self.logger = logger

        self.logger.debug("Initial setup done.")