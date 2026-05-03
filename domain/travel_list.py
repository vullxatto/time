"""Коллекция путёвок."""

from domain.entity_list import EntityList
from domain.package import Package


class TravelList(EntityList):

    def append_item(self, value):
        if isinstance(value, Package):
            super().append_item(value)

    def create_item(self, code, date='', quantity=0, discount=0):
        if code in self.get_codes():
            raise ValueError(f'Путёвка с кодом {code} уже существует.')
        p = Package(code, date, quantity, discount)
        p._library = getattr(self, '_parent_library', None)
        super().append_item(p)
        return p

    def new_item(self, date='', quantity=0, discount=0):
        p = Package(self.get_new_code(), date, quantity, discount)
        p._library = getattr(self, '_parent_library', None)
        super().append_item(p)
        return p
