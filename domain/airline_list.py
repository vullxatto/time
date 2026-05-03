"""Коллекция авиаперевозчиков."""

from domain.entity_list import EntityList
from domain.airline import Airline


class AirlineList(EntityList):

    def append_item(self, value):
        if isinstance(value, Airline):
            super().append_item(value)

    def create_item(self, code, name='', flight_cost=0):
        if code in self.get_codes():
            print(f'Авиаперевозчик с кодом {code} уже существует')
            return None
        a = Airline(code, name, flight_cost)
        super().append_item(a)
        return a

    def new_item(self, name='', flight_cost=0):
        a = Airline(self.get_new_code(), name, flight_cost)
        super().append_item(a)
        return a
