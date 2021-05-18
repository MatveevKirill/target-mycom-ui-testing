import pytest
import os
import random

from common.classes import Campaign
from common.classes import Segment


@pytest.fixture(scope="function")
def campaign_data(abs_path):
    campaign = Campaign.Campaign(
        name=f"Тестовая кампания #{random.randint(0, 1000)}",
        url="https://mail.ru/",
        ad_name="Название объявления",
        img_256x256_path=os.path.join(abs_path, "tmp", "imgs", "256x256.png"),
        ad_body="Текст объявления."
    )

    # Установить данные пола.
    campaign.SEX['MALE'] = True
    campaign.SEX['FEMALE'] = False

    # Установить географию.
    campaign.GEOGRAPHY.append("Россия")
    campaign.GEOGRAPHY.append("Бразилия")

    # Добавить информацию о 3 слайдах.
    campaign.add_slide(
        img_600x600_path=os.path.join(abs_path, "tmp", "imgs", "600x600.jpg"),
        header_slide_name="Название слайда 1",
        url="1.mail.ru"
    )
    campaign.add_slide(
        img_600x600_path=os.path.join(abs_path, "tmp", "imgs", "600x600.jpg"),
        header_slide_name="Название слайда 2",
        url="2.mail.ru"
    )
    campaign.add_slide(
        img_600x600_path=os.path.join(abs_path, "tmp", "imgs", "600x600.jpg"),
        header_slide_name="Название слайда 3",
        url="3.mail.ru"
    )

    return campaign


@pytest.fixture(scope="function")
def segments_data():
    segments = Segment.Segment()

    segments.add_segment(
        type="Приложения и игры в соцсетях",
        name=f"Тестовый сегмент #{random.randint(1, 1000)}",
        params={
            "play": True,
            "pay": True
        }
    )

    return segments
