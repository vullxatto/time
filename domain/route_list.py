"""Коллекция маршрутов."""

from domain.entity_list import EntityList
from domain.route import Route


class RouteList(EntityList):

    def append_item(self, value):
        if isinstance(value, Route):
            super().append_item(value)

    def create_item(self, code, name='', climate='', duration=0, hotel='', cost=0):
        if code in self.get_codes():
            print(f'Маршрут с кодом {code} уже существует')
            return None
        r = Route(code, name, climate, duration, hotel, cost)
        super().append_item(r)
        return r

    def new_item(self, name='', climate='', duration=0, hotel='', cost=0):
        r = Route(self.get_new_code(), name, climate, duration, hotel, cost)
        super().append_item(r)
        return r
