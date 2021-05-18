from selenium.webdriver.common.by import By


class LoginPageLocators(object):
    """
        Базовые локаторы для начальной страницы: https://target.my.com/.
        Данные локаторы не присутствуют на страницах после авторизации.
    """
    BUTTON_SIGN_IN = (By.XPATH, "//div[contains(@class, 'responseHead-module-button') and text() = 'Войти']")
    BUTTON_AUTH_FORM = (By.XPATH, "//div[contains(@class, 'authForm-module-button') and text() = 'Войти']")

    INPUT_USERNAME = (By.NAME, "email")
    INPUT_PASSWORD = (By.NAME, "password")

    LABEL_ERROR_NOTIFY_MODULE = (By.XPATH, "//div[contains(@class, 'notify-module-error')]")
    LABEL_ERROR_NOTIFY_MODULE_MYCOM = (By.XPATH, "//div[starts-with(@class, 'formMsg')]/div[@class = 'formMsg_text']")


class NavigationPanelLocatorsWithAuthorization(object):
    """
        Базовые локаторы для страниц после авторизации: https://target.my.com/dashboard/, etc.
        Данные локаторы присутствуют на страницах после авторизации:
            - Навигационное меню для перехода по страницам;
            - DropDown меню пользователя.
    """
    LABEL_USERNAME = (By.XPATH, "//div[contains(@class, 'right-module-userNameWrap')]")
    BUTTON_NAVIGATION_TEMPLATE = (By.XPATH, "//a[starts-with(@class, 'center-module-button-') and text() = '{}']")


class DashboardPageLocators(NavigationPanelLocatorsWithAuthorization):
    """
            Локаторы для работы с главной страницей после авторизации.
            Т.к. данная страница имеет локаторы основной страницы после авторизации, то необходимо наследование.
        """
    BUTTON_CREATE_FIRST_CAMPAIGN = (By.XPATH, "//a[text() = 'Создайте рекламную кампанию']")
    BUTTON_CREATE_CAMPAIGN = (By.XPATH, "//div[text() = 'Создать кампанию']")
    BUTTON_ICON_SETTINGS_TEMPLATE = (
        By.XPATH,
        "//div[@data-test = 'setting-{0} row-{0}']/div/div"
    )
    BUTTON_DELETE_CAMPAIGN = (
        By.XPATH,
        "//li[starts-with(@class, 'optionsList-module-option') and text() = 'Удалить']"
    )

    LINK_CAMPAIGN_TEMPLATE = (
        By.XPATH,
        "//a[starts-with(@class, 'nameCell-module-campaignNameLink') and text() = '{}']"
    )


class CampaignPageLocators(NavigationPanelLocatorsWithAuthorization):
    """
        Локаторы для работы с кампаниями.
        Т.к. данная страница имеет локаторы основной страницы после авторизации, то необходимо наследование.
    """
    BUTTON_TYPE_COVERAGE = (By.XPATH, "//div[text() = 'Охват']")
    BUTTON_SEX = (By.XPATH, "//li[@data-setting-name = 'sex']")
    BUTTON_SAVE_ADS = (By.XPATH, "//div[text() = 'Сохранить объявление']")
    BUTTON_CREATE_ADS_CAMPAIGN = (By.XPATH, "//div[@class = 'footer__button js-save-button-wrap']/button")
    BUTTON_CLEAR_REGIONS = (By.XPATH, "//span[starts-with(@class, 'region-module-resetAllBtn')]")
    BUTTON_REGION_ADD_TEMPLATE = (By.XPATH, "//li[starts-with(@class, 'suggester-module-option') and @title = '{}']")

    INPUT_COVERAGE_URL = (By.XPATH, "//input[starts-with(@class, 'mainUrl-module-searchInput-Su-Rad')]")
    INPUT_CAMPAIGN_NAME = (By.XPATH, "//div[contains(@class, 'input_campaign-name')]/div/input")
    INPUT_CAMPAIGN_REGION = (By.XPATH, "//input[@placeholder = 'Добавить или исключить регион']")
    INPUT_ADDRESS_URL = (By.XPATH, "//input[@placeholder = 'Введите адрес ссылки']")
    INPUT_ADS_HEADER = (By.XPATH, "//input[@placeholder = 'Введите заголовок объявления']")
    INPUT_ADS_BODY = (By.XPATH, "//textarea[@data-name = 'text_50' and @placeholder = 'Введите текст объявления']")
    INPUT_ADS_URL_TEMPLATE = (By.XPATH, "//input[@data-name = 'url_slide_{}']")
    INPUT_FILE_256X256 = (By.XPATH, "//input[@data-test = 'icon_256x256']")
    INPUT_FILE_600X600_TEMPLATE = (By.XPATH, "//input[@data-test = 'image_600x600_slide_{}']")
    INPUT_HEADER_ADS_TEMPLATE = (By.XPATH, "//input[@data-name = 'title_25_slide_{}']")

    LABEL_CAROUSEL = (By.ID, "patterns_26")
    LABEL_GEOGRAPHY_TEMPLATE = (
        By.XPATH,
        "//span[starts-with(@class, 'selectedRegions-module-regionName') and text() = '{}']"
    )
    LABEL_ADS_CAROUSEL_TEMPLATE = (
        By.XPATH,
        "(//div[starts-with(@class, 'carouselFull-module-textsWrap')]/div[starts-with(@class, '{}')])[2]"
    )
    LABEL_ADS_CAROUSEL_BODY = (
        By.XPATH,
        "(//div[starts-with(@class, 'carouselFull-module-wrapper')]/"
        "div[starts-with(@class, 'textBlockPreview-module-textBlock') and "
        "contains(@class, 'preview-module-previewText')])[2]"
    )
    LABEL_ADS_CAROUSEL_SLIDE_TEMPLATE = (
        By.XPATH,
        "(//div[@data-pattern-name = 'carousel_img_full_slide_{}']/div[4])[2]"
    )

    CHECKBOX_SEX_TEMPLATE = (By.XPATH, "//input[@targeting = 'sex-{}']")

    TAB_SLIDES = (By.XPATH, "//ul[starts-with(@class, 'roles-module-slidesTabs-')]")
    TAB_SLIDES_TEMPLATE = (By.XPATH, "//li[contains(@class, 'roles-module-slidesTabsItem') and @data-id = '{}']")


class SegmentsPageLocators(NavigationPanelLocatorsWithAuthorization):
    """
            Локаторы для работы с аудиториями (сегментами).
            Т.к. данная страница имеет локаторы основной страницы после авторизации, то необходимо наследование.
        """
    INPUT_SEGMENT_NAME = (
        By.XPATH,
        "//div[@class = 'input input_create-segment-form']/div/input"
    )

    BUTTON_CREATE_FIRST_SEGMENT = (By.XPATH, "//a[text() = 'Создайте']")
    BUTTON_ADDING_SEGMENT_ITEM_TEMPLATE = (
        By.XPATH,
        "//div[starts-with(@class, 'adding-segments-item') and text() = '{}']"
    )
    BUTTON_PLAYING_AND_PAID_IN_PLATFORM = (By.XPATH, "//div[@data-class-name='SourceView']")
    BUTTON_ADD_NEW_SEGMENT = (
        By.XPATH,
        "//div[starts-with(@class, 'segments-list__tbl-settings-wrap')]/div/button"
    )
    BUTTON_ADD_SEGMENT = (
        By.XPATH,
        "//div[@class = 'adding-segments-modal']/div[5]/div/button"
    )
    BUTTON_SUBMIT_CREATE_SEGMENT = (
        By.XPATH,
        "//div[starts-with(@class, 'create-segment-form__btn-wrap')]/button"
    )
    BUTTON_DELETE_SEGMENT = (
        By.XPATH,
        "//button[@class = 'button button_confirm-remove button_general']"
    )
    BUTTON_DELETE_SEGMENT_ICON_TEMPLATE = (
        By.XPATH,
        "//div[@data-test = 'remove-{0} row-{0}']/span"
    )

    CHECKBOX_IN_PLATFORM_TEMPLATE = (
        By.XPATH,
        "//input[starts-with(@class, 'segment-settings-view__checkbox') and @value = '{}']"
    )

    LINK_TO_SEGMENT_TEMPLATE = (By.XPATH, "//a[@title = '{}']")
