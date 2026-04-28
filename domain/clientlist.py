"""Коллекция клиентов."""

from domain.entitylist import entityList
from domain.client import client


class clientList(entityList):

    def appendItem(self, value):
        if isinstance(value, client):
            super().appendItem(value)

    def createItem(self, code, surname='', name='', secname='', address='', phone=''):
        if code in self.getCodes():
            print(f'Клиент с кодом {code} уже существует')
            return None
        c = client(code, surname, name, secname, address, phone)
        super().appendItem(c)
        return c

    def newItem(self, surname='', name='', secname='', address='', phone=''):
        c = client(self.getNewCode(), surname, name, secname, address, phone)
        super().appendItem(c)
        return c
