"""Маршрут (направление путешествия)."""

from domain.namedentity import namedentity


class route(namedentity):
    """Туристический маршрут с климатом, длительностью, отелем и стоимостью."""

    def __init__(self, code=0, name='', climate='', duration=0, hotel='', cost=0):
        super().__init__(code, name)
        self.setClimate(climate)
        self.setDuration(duration)
        self.setHotel(hotel)
        self.setCost(cost)

    def setClimate(self, value):
        self.__climate = value

    def setDuration(self, value):
        self.__duration = value

    def setHotel(self, value):
        self.__hotel = value

    def setCost(self, value):
        self.__cost = value

    def getClimate(self):
        return self.__climate

    def getDuration(self):
        return self.__duration

    def getHotel(self):
        return self.__hotel

    def getCost(self):
        return self.__cost
