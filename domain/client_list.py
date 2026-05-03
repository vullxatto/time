"""Коллекция клиентов."""

from domain.entity_list import EntityList
from domain.client import Client


class ClientList(EntityList):

    def append_item(self, value):
        if isinstance(value, Client):
            super().append_item(value)

    def create_item(self, code, surname='', name='', secname='', address='', phone=''):
        if code in self.get_codes():
            print(f'Клиент с кодом {code} уже существует')
            return None
        c = Client(code, surname, name, secname, address, phone)
        super().append_item(c)
        return c

    def new_item(self, surname='', name='', secname='', address='', phone=''):
        c = Client(self.get_new_code(), surname, name, secname, address, phone)
        super().append_item(c)
        return c
