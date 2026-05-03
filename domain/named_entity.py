"""Сущность, имеющая текстовое название (например, маршрут или авиаперевозчик)."""

from domain.entity import Entity


class NamedEntity(Entity):
    """Сущность с дополнительным текстовым атрибутом name."""

    def __init__(self, code=0, name=''):
        super().__init__(code)
        self.set_name(name)

    def set_name(self, value):
        self.__name = value

    def get_name(self):
        return self.__name
