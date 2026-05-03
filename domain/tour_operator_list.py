"""Коллекция туроператоров."""

from domain.entity_list import EntityList
from domain.tour_operator import TourOperator


class TourOperatorList(EntityList):

    def append_item(self, value):
        if isinstance(value, TourOperator):
            super().append_item(value)

    def create_item(self, code, name='', address='', phone='', website=''):
        if code in self.get_codes():
            print(f'Туроператор с кодом {code} уже существует')
            return None
        t = TourOperator(code, name, address, phone, website)
        super().append_item(t)
        return t

    def new_item(self, name='', address='', phone='', website=''):
        t = TourOperator(self.get_new_code(), name, address, phone, website)
        super().append_item(t)
        return t
