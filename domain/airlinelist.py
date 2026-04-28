"""Коллекция авиаперевозчиков."""

from domain.entitylist import entityList
from domain.airline import airline


class airlineList(entityList):

    def appendItem(self, value):
        if isinstance(value, airline):
            super().appendItem(value)

    def createItem(self, code, name='', flight_cost=0):
        if code in self.getCodes():
            print(f'Авиаперевозчик с кодом {code} уже существует')
            return None
        a = airline(code, name, flight_cost)
        super().appendItem(a)
        return a

    def newItem(self, name='', flight_cost=0):
        a = airline(self.getNewCode(), name, flight_cost)
        super().appendItem(a)
        return a
