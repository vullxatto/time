"""Маршрут (направление путешествия)."""

from domain.named_entity import NamedEntity


class Route(NamedEntity):
    """Туристический маршрут с климатом, длительностью, отелем и стоимостью."""

    def __init__(self, code=0, name='', climate='', duration=0, hotel='', cost=0):
        super().__init__(code, name)
        self.set_climate(climate)
        self.set_duration(duration)
        self.set_hotel(hotel)
        self.set_cost(cost)

    def set_climate(self, value):
        self.__climate = value

    def set_duration(self, value):
        self.__duration = value

    def set_hotel(self, value):
        self.__hotel = value

    def set_cost(self, value):
        self.__cost = value

    def get_climate(self):
        return self.__climate

    def get_duration(self):
        return self.__duration

    def get_hotel(self):
        return self.__hotel

    def get_cost(self):
        return self.__cost
