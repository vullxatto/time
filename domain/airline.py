"""Авиаперевозчик — авиакомпания, выполняющая перелёт по путёвке."""

from domain.namedentity import namedentity


class airline(namedentity):
    """Авиакомпания со стоимостью авиаперелёта."""

    def __init__(self, code=0, name='', flight_cost=0):
        super().__init__(code, name)
        self.setFlightCost(flight_cost)

    def setFlightCost(self, value):
        self.__flight_cost = value

    def getFlightCost(self):
        return self.__flight_cost
