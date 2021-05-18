import allure
from selenium.common import exceptions

from ui.pages.base_page import BasePageActions
from ui.locators.page_locators import LoginPageLocators

from common import exceptions as CE
from common.classes.URL import PageURL


class LoginPage(BasePageActions):
    """ Основная страница без авторизации. """
    url = PageURL.BASE_URL
    locators = LoginPageLocators()

    @allure.step("Checking user credentials: {username}:{password}")
    def login(self, username: str, password: str):
        # Авторизация на сервисе myTarget, используя ActionChains.
        self.click(locator=self.locators.BUTTON_SIGN_IN)

        # Ввод данных для авторизации
        self.send_keys(locator=self.locators.INPUT_USERNAME, send_data=str(username))
        self.send_keys(locator=self.locators.INPUT_PASSWORD, send_data=str(password))

        # Кнопка авторизации.
        self.click(locator=self.locators.BUTTON_AUTH_FORM)

        # Проверка перехода на нужную страницу после авторизации.
        try:
            self._is_opened(is_opened_params={"new_url": PageURL.DASHBOARD})
            return
        except TimeoutError:
            pass

        # Поиск ошибок при авторизации:
        # * Проверка на ошибку: "Введите email или телефон".
        try:
            ex_msg = self.get_text_from_element(locator=self.locators.LABEL_ERROR_NOTIFY_MODULE, timeout=2)
            raise CE.AuthorizationException(f"Not verified user '{username}'. Error: {ex_msg}.")
        except exceptions.TimeoutException:
            pass
        # * Проверка на ошибку на стороннем сайте my.com: "Неверный логин или пароль".
        try:
            ex_msg = self.find_element(locator=self.locators.LABEL_ERROR_NOTIFY_MODULE_MYCOM, timeout=2)
            raise CE.AuthorizationException(f"not verified user '{username}'. Error: {ex_msg}.")
        except exceptions.TimeoutException:
            pass
