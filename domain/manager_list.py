"""Коллекция менеджеров."""

from domain.entity_list import EntityList
from domain.manager import Manager


class ManagerList(EntityList):

    def append_item(self, value):
        if isinstance(value, Manager):
            super().append_item(value)

    def create_item(self, code, surname='', name='', secname='',
                   position='', phone='', email=''):
        if code in self.get_codes():
            print(f'Менеджер с кодом {code} уже существует')
            return None
        m = Manager(code, surname, name, secname, position, phone, email)
        super().append_item(m)
        return m

    def new_item(self, surname='', name='', secname='',
                position='', phone='', email=''):
        m = Manager(self.get_new_code(), surname, name, secname, position, phone, email)
        super().append_item(m)
        return m
