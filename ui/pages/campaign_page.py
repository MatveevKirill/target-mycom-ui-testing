from selenium.webdriver import Chrome
from selenium.common import exceptions

from ui.pages.base_page import BasePageActions
from ui.locators.page_locators import CampaignPageLocators

from common.classes.Campaign import Campaign
from common.classes.URL import PageURL
from common import exceptions as CE


class CampaignPage(BasePageActions):
    url = None
    locators = CampaignPageLocators()

    def __init__(self, driver: Chrome, configuration: dict, url_param: str = "", is_opened_params: dict = None) -> None:
        """
        При инициализации страницы "Кампании" необходимо создавать URL в зависимости от того, на какой подстранице
        находимся в данный момент. Также URL может быть динамическим (для страницы с конкретной компанией).
        :param driver: драйвер Chrome.
        :param configuration: конфигурация тестирования.
        :param url_param: параметр url, который вставляется после строки https://target.my.com/campaign/...
        :param is_opened_params: параметры для проверки открытия url страницы.
        """
        self.url = PageURL.CAMPAIGN_TEMPLATE.format(url_param)
        super().__init__(driver=driver, configuration=configuration, is_opened_params=is_opened_params)

    def create_campaign(self, campaign: Campaign) -> None:
        """
        Метод для создания кампании на через страницу Dashboard.
        :param campaign: информация о кампании.
        :return: None
        """

        # Выбираем вариант "Охват".
        self.click(locator=self.locators.BUTTON_TYPE_COVERAGE)

        # Отправляем URL на страницу и проверяем на ошибки ввода.
        self.send_keys(locator=self.locators.INPUT_COVERAGE_URL, send_data=campaign.URL)

        # Отправляем название компании.
        self.scroll_to(locator=self.locators.INPUT_CAMPAIGN_NAME)
        self.send_keys(locator=self.locators.INPUT_CAMPAIGN_NAME, send_data=campaign.NAME)

        # Отправляем данные по полу потребителей.
        self.scroll_to(locator=self.locators.BUTTON_SEX)
        self.click(locator=self.locators.BUTTON_SEX)
        if not campaign.SEX['MALE']:
            self.click(
                locator=(
                    self.locators.CHECKBOX_SEX_TEMPLATE[0],
                    self.locators.CHECKBOX_SEX_TEMPLATE[1].format('male')
                )
            )
        if not campaign.SEX['FEMALE']:
            self.click(
                locator=(
                    self.locators.CHECKBOX_SEX_TEMPLATE[0],
                    self.locators.CHECKBOX_SEX_TEMPLATE[1].format('female')
                )
            )

        # Сбросить всю информацию по регионам, если автоматически устанавливаются страны.
        try:
            # Если кнопка на найдена, значит всё уже очищено.
            self.click(locator=self.locators.BUTTON_CLEAR_REGIONS)
        except exceptions.TimeoutException:
            pass

        # Добавить регионы.
        self.scroll_to(locator=self.locators.INPUT_CAMPAIGN_REGION)
        for region in campaign.GEOGRAPHY:
            self.send_keys(locator=self.locators.INPUT_CAMPAIGN_REGION, send_data=region)
            self.click(
                locator=(
                    self.locators.BUTTON_REGION_ADD_TEMPLATE[0],
                    self.locators.BUTTON_REGION_ADD_TEMPLATE[1].format(region)
                )
            )

        # Выбрать вариант показа "Карусель".
        self.click(locator=self.locators.LABEL_CAROUSEL)

        # Добавление информации по слайдам.
        i = 0
        for slide in campaign.SLIDES:
            # Переключаемся между слайдами.
            self.click(
                locator=(
                    self.locators.TAB_SLIDES_TEMPLATE[0],
                    self.locators.TAB_SLIDES_TEMPLATE[1].format(i)
                )
            )

            # Отправляем данные о url слайда.
            self.send_keys(
                locator=(
                    self.locators.INPUT_ADS_URL_TEMPLATE[0],
                    self.locators.INPUT_ADS_URL_TEMPLATE[1].format(i + 1)
                ),
                send_data=slide['url']
            )

            # Отправляем данные о заголовке слайда.
            self.send_keys(
                locator=(
                    self.locators.INPUT_HEADER_ADS_TEMPLATE[0],
                    self.locators.INPUT_HEADER_ADS_TEMPLATE[1].format(i + 1)
                ),
                send_data=slide['header_slide_name']
            )

            # Отправляем данные о фото 600x600 px.
            self.find_element(
                locator=(
                    self.locators.INPUT_FILE_600X600_TEMPLATE[0],
                    self.locators.INPUT_FILE_600X600_TEMPLATE[1].format(i + 1)
                )
            ).send_keys(slide['img_600x600_path'])

            i += 1

        # Добавление информации об объявлении.
        self.send_keys(locator=self.locators.INPUT_ADDRESS_URL, send_data=campaign.URL)
        self.send_keys(locator=self.locators.INPUT_ADS_HEADER, send_data=campaign.AD_NAME)

        # Отправка изображения 256x256.
        self.find_element(locator=self.locators.INPUT_FILE_256X256).send_keys(campaign.IMG_256X256_PATH)

        # Ввод текста сообщения.
        self.send_keys(locator=self.locators.INPUT_ADS_BODY, send_data=campaign.AD_BODY)

        # Сохранения объявления.
        self.scroll_to(locator=self.locators.BUTTON_SAVE_ADS)
        self.click(locator=self.locators.BUTTON_SAVE_ADS)

        # Создание компании.
        self.click(locator=self.locators.BUTTON_CREATE_ADS_CAMPAIGN)

        # Ожидание создания кампании и автоматический переход на главную страницу
        self._is_opened(is_opened_params={"new_url": PageURL.DASHBOARD, "ignore_get_params": True})

        dashboard = self.go_to('dashboard')

        # Проверка существования на странице названия кампании.
        try:
            dashboard.find_element(
                locator=(
                    dashboard.locators.LINK_CAMPAIGN_TEMPLATE[0],
                    dashboard.locators.LINK_CAMPAIGN_TEMPLATE[1].format(campaign.NAME)
                )
            )
        except exceptions.TimeoutException:
            raise CE.ImpossibleToCreateObjectException(f"Campaign '{campaign.NAME}' not been created.")

    def delete_campaign(self, campaign: Campaign) -> None:
        dashboard = self.go_to('dashboard')

        # * Получение данных об ID элемента.
        campaign_id = self.get_attr_from_element(
            attribute_name="href",
            locator=(dashboard.locators.LINK_CAMPAIGN_TEMPLATE[0],
                     dashboard.locators.LINK_CAMPAIGN_TEMPLATE[1].format(campaign.NAME))
        ).split("?")[0].split("/")[::-1][0]

        dashboard.click(
            locator=(dashboard.locators.BUTTON_ICON_SETTINGS_TEMPLATE[0],
                     dashboard.locators.BUTTON_ICON_SETTINGS_TEMPLATE[1].format(campaign_id))
        )
        dashboard.click(locator=dashboard.locators.BUTTON_DELETE_CAMPAIGN)

        # Перезагрузка страницы.
        dashboard.refresh()
