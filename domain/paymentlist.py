"""Коллекция платежей."""

from domain.entitylist import entityList
from domain.payment import payment


class paymentList(entityList):

    def appendItem(self, value):
        if isinstance(value, payment):
            super().appendItem(value)

    def createItem(self, code, package_code=0, date='', amount=0,
                   method='', status='в ожидании'):
        if code in self.getCodes():
            print(f'Платёж с кодом {code} уже существует')
            return None
        p = payment(code, package_code, date, amount, method, status)
        super().appendItem(p)
        return p

    def newItem(self, package_code=0, date='', amount=0,
                method='', status='в ожидании'):
        p = payment(self.getNewCode(), package_code, date, amount, method, status)
        super().appendItem(p)
        return p

    def findByPackage(self, package_code):
        """Платёж за заданную путёвку (1:1) или None."""
        for p in self.getItems():
            if p.getPackageCode() == package_code:
                return p
        return None
