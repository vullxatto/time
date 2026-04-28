"""Коллекция путёвок."""

from domain.entitylist import entityList
from domain.package import package


class travelList(entityList):

    def appendItem(self, value):
        if isinstance(value, package):
            super().appendItem(value)

    def createItem(self, code, date='', quantity=0, discount=0):
        if code in self.getCodes():
            print(f'Путёвка с кодом {code} уже существует')
            return None
        p = package(code, date, quantity, discount)
        p._library = getattr(self, '_parent_library', None)
        super().appendItem(p)
        return p

    def newItem(self, date='', quantity=0, discount=0):
        p = package(self.getNewCode(), date, quantity, discount)
        p._library = getattr(self, '_parent_library', None)
        super().appendItem(p)
        return p
