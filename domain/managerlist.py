"""Коллекция менеджеров."""

from domain.entitylist import entityList
from domain.manager import manager


class managerList(entityList):

    def appendItem(self, value):
        if isinstance(value, manager):
            super().appendItem(value)

    def createItem(self, code, surname='', name='', secname='',
                   position='', phone='', email=''):
        if code in self.getCodes():
            print(f'Менеджер с кодом {code} уже существует')
            return None
        m = manager(code, surname, name, secname, position, phone, email)
        super().appendItem(m)
        return m

    def newItem(self, surname='', name='', secname='',
                position='', phone='', email=''):
        m = manager(self.getNewCode(), surname, name, secname, position, phone, email)
        super().appendItem(m)
        return m
