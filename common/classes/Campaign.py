class Campaign(object):
    # Название кампании.
    NAME = ""

    # Название объявления.
    AD_NAME = ""

    # Объявление.
    AD_BODY = ""

    # Ссылка на сайт.
    URL = ""

    # Гендер потребителей.
    SEX = {"MALE": True, "FEMALE": True}

    # Ругионы показа рекламы.
    GEOGRAPHY = []

    # Слайды.
    SLIDES = []

    # Ссылка на изображение 256x256 px.
    IMG_256X256_PATH = ""

    def __init__(self, name: str, url: str, ad_name: str, img_256x256_path: str, ad_body: str):
        self.NAME = name
        self.URL = url
        self.AD_NAME = ad_name
        self.IMG_256X256_PATH = img_256x256_path
        self.AD_BODY = ad_body

    def add_slide(self, img_600x600_path: str, header_slide_name: str, url: str) -> None:
        """
        Добавить слайд в объявление.
        :param img_600x600_path: ссылка на изображение 600x600 px.
        :param header_slide_name: название слайда.
        :param url: ссылка слайда.
        :return: None
        """
        if self.SLIDES == 6:
            return

        self.SLIDES.append(
            {
                "img_600x600_path": img_600x600_path,
                "header_slide_name": header_slide_name,
                "url": url
            }
        )

    def remove_slide(self, num: int) -> None:
        """
        Удаление слайда.
        :param num: номер слайда.
        :return: None
        """
        if num > len(self.SLIDES):
            return
        self.SLIDES.pop(num - 1)
