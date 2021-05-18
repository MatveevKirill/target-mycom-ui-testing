import allure
import pytest
from selenium.common import exceptions

from creds import Credentials
from tests.base_test import BaseTestCase
from common import exceptions as CE

from ui.pages.dashboard_page import DashboardPage
from ui.pages.campaign_page import CampaignPage
from ui.pages.segments_page import SegmentsPage

from common.classes.Campaign import Campaign
from common.classes.Segment import Segment


class TestCaseAuthorization(BaseTestCase):

    @allure.epic("Authorization tests")
    @allure.feature("Positive tests")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.UI
    def test_login_positive(self, dashboard: DashboardPage) -> None:
        self.logger.info("Use positive login.")
        creds = Credentials()

        # В данном тесте используется фикстура 'dashboard' с автоматической авторизацией.
        # Проверка на корректность авторизации.
        username = dashboard.get_text_from_element(locator=dashboard.locators.LABEL_USERNAME).lower()
        with allure.step("Checking positive user credentials"):
            assert username == creds.LOGIN or username == "матвеев кирилл алексеевич"

    @allure.epic("Authorization tests")
    @allure.feature("Negative tests")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("username, password", [("test", "wrong-email-type"), ("8999", "wrong-phone")])
    @pytest.mark.UI
    def test_login_negative(self, username: str, password: str, login_page) -> None:
        self.logger.info("Use negative login.")
        with allure.step("Checking negative credentials"):
            with pytest.raises(CE.AuthorizationException):
                login_page.login(username=username, password=password)
                pytest.fail(f"Input valid credentials (username='{username}', password='{password}')")


class TestCaseCampaign(BaseTestCase):

    @allure.epic("Campaign tests")
    @pytest.mark.UI
    def test_create_campaign(self, dashboard: DashboardPage, campaign_data: Campaign) -> None:
        # Переходим на страницу создания кампаниию.
        # После создания кампании происходит автоматический редирект на страницу Dashboard.
        self.logger.debug(f"Attempting to create a campaign: {campaign_data.NAME}")
        dashboard.go_to_create_campaign().create_campaign(campaign=campaign_data)
        self.logger.debug(f"Campaign created: {campaign_data.NAME}")

        # Переход на страницу с кампанией для проверки корректности данных.
        campaign: CampaignPage = dashboard.go_to_campaign(campaign_name=campaign_data.NAME)

        # Проверка названия компании.
        with allure.step("Check campaign name"):
            assert campaign.get_attr_from_element(
                attribute_name="value",
                locator=campaign.locators.INPUT_CAMPAIGN_NAME
            ) == campaign_data.NAME

        # Проверка пола потребителей.
        with allure.step("Check gender"):
            for gender in ["male", "female"]:
                with allure.step(f"Check gender: {gender}"):
                    assert campaign.get_selected_from_element(
                        locator=(campaign.locators.CHECKBOX_SEX_TEMPLATE[0],
                                 campaign.locators.CHECKBOX_SEX_TEMPLATE[1].format(gender))
                    ) == campaign_data.SEX[gender.upper()]

        # Проверка регионов.
        with allure.step(f"Check regions"):
            count_regions = len(campaign_data.GEOGRAPHY)
            for region in campaign_data.GEOGRAPHY:
                try:
                    with allure.step(f"Region: {region}"):
                        campaign.find_element(
                            locator=(
                                campaign.locators.LABEL_GEOGRAPHY_TEMPLATE[0],
                                campaign.locators.LABEL_GEOGRAPHY_TEMPLATE[1].format(region)
                            )
                        )
                        # Проверка на количество регионов в блоке.
                        count_regions -= 1
                        if count_regions < 0:
                            pytest.fail(f"Too many regions in block (region='{region}').")
                except exceptions.TimeoutException:
                    pytest.fail(f"Could not find region '{region}'.")

        # Проверка названия объявления.
        with allure.step("Check name ads"):
            assert campaign.get_text_from_element(
                locator=(campaign.locators.LABEL_ADS_CAROUSEL_TEMPLATE[0],
                         campaign.locators.LABEL_ADS_CAROUSEL_TEMPLATE[1].format('textBlockPreview-module-textBlock'))
            ) == campaign_data.AD_NAME

        # Проверка сссылки объявления.
        with allure.step("Check url ads"):
            assert campaign.get_text_from_element(
                locator=(campaign.locators.LABEL_ADS_CAROUSEL_TEMPLATE[0],
                         campaign.locators.LABEL_ADS_CAROUSEL_TEMPLATE[1].format('urlPreview-module-url'))
            ) == campaign_data.URL

        # Проверка текста объявления.
        with allure.step("Check body ads"):
            assert campaign.get_text_from_element(
                locator=campaign.locators.LABEL_ADS_CAROUSEL_BODY
            ) == campaign_data.AD_BODY

        # Удаление рекламной кампании.
        self.logger.debug(f"Attempting to delete a campaign: {campaign_data.NAME}")

        campaign.go_to("dashboard")
        campaign.delete_campaign(campaign_data)
        self.logger.debug(f"Removed campaign: {campaign_data.NAME}")

        # Поиск названия кампании после удаления.
        with pytest.raises(exceptions.TimeoutException):
            dashboard.find_element(
                locator=(dashboard.locators.LINK_CAMPAIGN_TEMPLATE[0],
                         dashboard.locators.LINK_CAMPAIGN_TEMPLATE[1].format(campaign_data.NAME))
            )
        self.logger.debug(f"Checked the deletion of the campaign: {campaign_data.NAME}")


class TestCaseSegments(BaseTestCase):

    @allure.epic("Segments tests")
    @allure.story("Create segment")
    @pytest.mark.UI
    def test_create_segment(self, dashboard: DashboardPage, segments_data: Segment) -> None:
        # Переход на страницу Аудитории
        segments: SegmentsPage = dashboard.go_to("segments")

        # Создание сегмента.
        self.logger.debug(f"Attempting to create a segment: {segments_data.NAME}")
        segments.create_segment(segment=segments_data)
        self.logger.debug(f"Segment created: {segments_data.NAME}")

        # Получение ID сегмента:
        segment_id = segments.check_create_segment(segments_data)

        # Удаление сегмента.
        self.logger.debug(f"Attempting to delete a segment: {segments_data.NAME}")
        segments.click(locator=(segments.locators.BUTTON_DELETE_SEGMENT_ICON_TEMPLATE[0],
                                segments.locators.BUTTON_DELETE_SEGMENT_ICON_TEMPLATE[1].format(segment_id)))
        segments.click(locator=segments.locators.BUTTON_DELETE_SEGMENT)
        self.logger.debug(f"Removed segment: {segments_data.NAME}")

        import time
        time.sleep(4)

    @allure.epic("Segments tests")
    @allure.story("Deleting a segment")
    @pytest.mark.UI
    def test_delete_segment(self, dashboard: DashboardPage, segments_data: Segment) -> None:
        # Переход на страницу Аудитории
        segments: SegmentsPage = dashboard.go_to("segments")

        # Создание сегмента.
        self.logger.debug(f"Attempting to create a segment: {segments_data.NAME}")
        segments.create_segment(segment=segments_data)
        self.logger.debug(f"Segment created: {segments_data.NAME}")

        # Удаление сегмента
        with allure.step(f"Deleting a segment '{segments_data.NAME}' from a page"):
            try:
                segments.delete_segment(segment_name=segments_data.NAME)
            except CE.CannotUseActionChains as e:
                pytest.fail(f'Cannot delete segment. Error: {e.args[0]}')
