"""Расширенная коллекция путёвок: создаёт PackageExt вместо package."""

from domain.travel_list import TravelList
from domain.package_ext import PackageExt


class TravelListExt(TravelList):

    def create_item(self, code, date='', quantity=0, discount=0,
                   airline_code=0, touroperator_code=0, manager_code=0):
        if code in self.get_codes():
            print(f'Путёвка с кодом {code} уже существует')
            return None
        p = PackageExt(code, date, quantity, discount,
                        airline_code, touroperator_code, manager_code)
        p._library = getattr(self, '_parent_library', None)
        # Используем append_item базового класса (EntityList), минуя проверку типа
        # из TravelList — PackageExt тоже является package, проверка пройдёт.
        super().append_item(p)
        return p

    def new_item(self, date='', quantity=0, discount=0,
                airline_code=0, touroperator_code=0, manager_code=0):
        p = PackageExt(self.get_new_code(), date, quantity, discount,
                        airline_code, touroperator_code, manager_code)
        p._library = getattr(self, '_parent_library', None)
        super().append_item(p)
        return p
