"""Базовая модель туристической фирмы.

Содержит три ключевые сущности предметной области — клиентов, маршруты и
путёвки — и предоставляет операции CRUD над ними. Расширенные сущности
(авиаперевозчики, туроператоры, менеджеры, платежи) добавляются в подклассе.
"""

from domain.client_list import ClientList
from domain.route_list import RouteList
from domain.travel_list import TravelList


class TravelCompany:
    """Хранит коллекции клиентов, маршрутов и путёвок и предоставляет к ним доступ."""

    def __init__(self):
        self._client_list = ClientList()
        self._route_list = RouteList()
        self._travel_list = TravelList()
        self._travel_list._parent_library = self

    def clear(self):
        self._client_list.clear()
        self._route_list.clear()
        self._travel_list.clear()

    # --- клиенты ---
    def create_client(self, code, surname='', name='', secname='', address='', phone=''):
        return self._client_list.create_item(
            code, surname, name, secname, address, phone)

    def new_client(self, surname='', name='', secname='', address='', phone=''):
        return self._client_list.new_item(surname, name, secname, address, phone)

    def remove_client(self, value):
        self._client_list.remove_item(value)
        for p in self._travel_list.get_items():
            p.remove_client(value)

    def get_client(self, code):
        return self._client_list.find_by_code(code)

    def get_client_list(self):
        return self._client_list.get_items()

    def get_client_codes(self):
        return self._client_list.get_codes()

    def get_client_new_code(self):
        return self._client_list.get_new_code()

    # --- маршруты ---
    def create_route(self, code, name='', climate='', duration=0, hotel='', cost=0):
        return self._route_list.create_item(code, name, climate, duration, hotel, cost)

    def new_route(self, name='', climate='', duration=0, hotel='', cost=0):
        return self._route_list.new_item(name, climate, duration, hotel, cost)

    def remove_route(self, value):
        self._route_list.remove_item(value)
        for p in self._travel_list.get_items():
            p.remove_route(value)

    def get_route(self, code):
        return self._route_list.find_by_code(code)

    def get_route_list(self):
        return self._route_list.get_items()

    def get_route_codes(self):
        return self._route_list.get_codes()

    def get_route_new_code(self):
        return self._route_list.get_new_code()

    # --- путёвки ---
    def create_travel(self, code, date='', quantity=0, discount=0):
        travel = self._travel_list.create_item(code, date, quantity, discount)
        if travel:
            travel._library = self
        return travel

    def new_travel(self, date='', quantity=0, discount=0):
        travel = self._travel_list.new_item(date, quantity, discount)
        if travel:
            travel._library = self
        return travel

    def remove_travel(self, value):
        self._travel_list.remove_item(value)

    def get_travel(self, code):
        return self._travel_list.find_by_code(code)

    def get_travel_list(self):
        return self._travel_list.get_items()

    def get_travel_codes(self):
        return self._travel_list.get_codes()

    def get_travel_new_code(self):
        return self._travel_list.get_new_code()
