from selenium.webdriver import Chrome
from selenium.common import exceptions

from ui.pages.base_page import BasePageActions
from ui.locators.page_locators import SegmentsPageLocators

from common import exceptions as CE
from common.classes.Segment import Segment
from common.classes.URL import PageURL


class SegmentsPage(BasePageActions):
    url = None
    locators = SegmentsPageLocators()

    def __init__(self, driver: Chrome, configuration: dict, url_param: str = "") -> None:
        self._change_url(url_param=url_param, is_opened_verify=False)
        super().__init__(driver=driver, configuration=configuration)

    def _change_url(self, url_param: str = "", is_opened_verify: bool = True) -> None:
        self.url = PageURL.SEGMENTS_TEMPLATE.format(url_param)
        if is_opened_verify:
            self._is_opened()

    def create_segment(self, segment: Segment) -> None:
        try:
            self.click(locator=self.locators.BUTTON_CREATE_FIRST_SEGMENT)
            # Меняем URL страницы для перехода.
            self._change_url("/new/")
        except exceptions.ElementNotInteractableException:
            self.click(locator=self.locators.BUTTON_ADD_NEW_SEGMENT)
            # Меняем URL страницы для перехода.
            self._change_url("/new")

        # Выбрать кнопку "Приложения и игры в соцсетях".
        self.click(locator=(self.locators.BUTTON_ADDING_SEGMENT_ITEM_TEMPLATE[0],
                            self.locators.BUTTON_ADDING_SEGMENT_ITEM_TEMPLATE[1].format(segment.TYPE)))

        # Выбрать подменю "Игравшие и платившие в платформе".
        self.click(locator=self.locators.BUTTON_PLAYING_AND_PAID_IN_PLATFORM)

        # Установить параметры для сегмента.
        for key in segment.PARAMS.keys():
            checkbox = self.find_element(locator=(
                self.locators.CHECKBOX_IN_PLATFORM_TEMPLATE[0],
                self.locators.CHECKBOX_IN_PLATFORM_TEMPLATE[1].format(key)
            ))
            # Сбрасываем настройки checkbox.
            if checkbox.is_selected(): checkbox.click()

            # Устанавливаем флаг только для нужного элемента.
            if segment.PARAMS[key]:
                checkbox.click()

        # Нажимаем на кнопку "Добавитьс сегмент"
        self.click(locator=self.locators.BUTTON_ADD_SEGMENT)

        # Установить имя для сегмента.
        self.send_keys(locator=self.locators.INPUT_SEGMENT_NAME, send_data=segment.NAME)

        # Нажать на кнопку "Создать сегмент".
        self.click(locator=self.locators.BUTTON_SUBMIT_CREATE_SEGMENT)

        # Сменить URL на базовый.
        self._change_url("")

    def delete_segment(self, segment_name: str) -> None:
        # Получение ID сегмента.
        segment_id = self.get_attr_from_element(
            attribute_name="href",
            locator=(self.locators.LINK_TO_SEGMENT_TEMPLATE[0],
                     self.locators.LINK_TO_SEGMENT_TEMPLATE[1].format(segment_name))
        ).split('?')[0].split('/')[::-1][0]

        # Удаление сегмента.
        self.click(locator=(self.locators.BUTTON_DELETE_SEGMENT_ICON_TEMPLATE[0],
                            self.locators.BUTTON_DELETE_SEGMENT_ICON_TEMPLATE[1].format(segment_id)))
        self.click(locator=self.locators.BUTTON_DELETE_SEGMENT)

        # Обновление страницы.
        self.refresh()

        # Проверка удаления сегмента.
        try:
            self.find_element(
                locator=(self.locators.LINK_TO_SEGMENT_TEMPLATE[0],
                         self.locators.LINK_TO_SEGMENT_TEMPLATE[1].format(segment_name))
                )
            raise CE.ImpossibleToDeleteObjectException(f'Segment "{segment_name}" did not deleted.')
        except exceptions.TimeoutException:
            pass

    def check_create_segment(self, segment: Segment) -> str:
        # Проверка наличия на странице.
        try:
            # * Получение ID сегмента.
            return self.get_attr_from_element(
                attribute_name="href",
                locator=(self.locators.LINK_TO_SEGMENT_TEMPLATE[0],
                         self.locators.LINK_TO_SEGMENT_TEMPLATE[1].format(segment.NAME))
            ).split("?")[0].split("/")[::-1][0]
        except exceptions.TimeoutException:
            raise CE.ImpossibleToCreateObjectException(f"Segment '{segment.NAME}' not been created.")