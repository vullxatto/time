"""Коллекция платежей."""

from domain.entity_list import EntityList
from domain.payment import Payment


class PaymentList(EntityList):

    def append_item(self, value):
        if isinstance(value, Payment):
            super().append_item(value)

    def create_item(self, code, package_code=0, date='', amount=0,
                   method='', status='в ожидании'):
        if code in self.get_codes():
            raise ValueError(f'Платёж с кодом {code} уже существует.')
        p = Payment(code, package_code, date, amount, method, status)
        super().append_item(p)
        return p

    def new_item(self, package_code=0, date='', amount=0,
                method='', status='в ожидании'):
        p = Payment(self.get_new_code(), package_code, date, amount, method, status)
        super().append_item(p)
        return p

    def find_by_package(self, package_code):
        """Платёж за заданную путёвку (1:1) или None."""
        for p in self.get_items():
            if p.get_package_code() == package_code:
                return p
        return None
