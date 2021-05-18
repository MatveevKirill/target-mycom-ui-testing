from selenium.common import exceptions

from ui.pages.base_page import BasePageActions
from ui.pages.campaign_page import CampaignPage
from ui.locators.page_locators import DashboardPageLocators

from common.classes.URL import PageURL


class DashboardPage(BasePageActions):
    url = PageURL.DASHBOARD
    locators = DashboardPageLocators()

    def go_to_create_campaign(self) -> CampaignPage:
        # При создании кампании может быть две ситуации:
        # *Если пользователь не создавал ранее кампании, то будет отображаться кнопка "Создайте рекламную компанию".
        # *Если пользователь создавал ранее кампании, то на странице всегда будет отображаться кнопка "Создать компанию"
        self.write_log(f"Going to: '{CampaignPage.__class__.__name__}'. URL: '{self.url}'.")
        try:
            self.click(locator=self.locators.BUTTON_CREATE_FIRST_CAMPAIGN)
        except exceptions.TimeoutException:
            self.click(locator=self.locators.BUTTON_CREATE_CAMPAIGN)

        return CampaignPage(driver=self.driver, configuration=self.configuration, url_param="new")

    def go_to_campaign(self, campaign_name: str) -> CampaignPage:
        self.write_log(f"Going to: '{CampaignPage.__class__.__name__}'. URL: '{self.url}'.")
        self.click(
            locator=(
                self.locators.LINK_CAMPAIGN_TEMPLATE[0],
                self.locators.LINK_CAMPAIGN_TEMPLATE[1].format(campaign_name)
            )
        )

        # Сменить активное окно.
        self.switch_tab(1, close_prev=True)

        return CampaignPage(
            driver=self.driver,
            configuration=self.configuration,
            url_param=str(self.driver.current_url.split("?")[0].split("/")[::-1][0]),
            is_opened_params={"ignore_get_params": True}
        )
