"""Сущность, имеющая текстовое название (например, маршрут или авиаперевозчик)."""

from domain.entity import entity


class namedentity(entity):
    """Сущность с дополнительным текстовым атрибутом name."""

    def __init__(self, code=0, name=''):
        super().__init__(code)
        self.setName(name)

    def setName(self, value):
        self.__name = value

    def getName(self):
        return self.__name
