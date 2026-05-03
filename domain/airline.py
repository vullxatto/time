"""Авиаперевозчик — авиакомпания, выполняющая перелёт по путёвке."""

from domain.named_entity import NamedEntity


class Airline(NamedEntity):
    """Авиакомпания со стоимостью авиаперелёта."""

    def __init__(self, code=0, name='', flight_cost=0):
        super().__init__(code, name)
        self.set_flight_cost(flight_cost)

    def set_flight_cost(self, value):
        self.__flight_cost = value

    def get_flight_cost(self):
        return self.__flight_cost
