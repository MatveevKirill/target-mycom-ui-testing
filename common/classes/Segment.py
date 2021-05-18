class Segment(object):
    # Название сегмента.
    NAME = ""

    # Тип сегмента.
    TYPE = ""

    # Параметры для сегмента.
    PARAMS = None

    def __init__(self):
        pass

    def add_segment(self, name: str, type: str, params: dict = None) -> None:
        """
        Добавление сегмента.
        :param name: название сегмента.
        :param type: тип сегмента.
        :param params: параметры сегмента.
        :return: None
        """
        self.TYPE = type
        self.NAME = name
        self.PARAMS = params
