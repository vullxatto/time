"""Расширенная модель турфирмы.

Базовый ``TravelCompany`` отвечает за три ключевые сущности предметной области
(клиенты, маршруты, путёвки). Подкласс ``TravelCompanyExt`` дополняет модель
ещё четырьмя через наследование, не затрагивая базовый API:

  - авиаперевозчики (FK 1:N от путёвки)
  - туроператоры    (FK 1:N от путёвки)
  - менеджеры       (FK 1:N от путёвки)
  - платежи         (1:1 к путёвке через FK package_code)
"""

from domain.travel_company import TravelCompany
from domain.travel_list_ext import TravelListExt
from domain.airline_list import AirlineList
from domain.tour_operator_list import TourOperatorList
from domain.manager_list import ManagerList
from domain.payment_list import PaymentList


class TravelCompanyExt(TravelCompany):

    def __init__(self):
        super().__init__()
        # Подменяем приватный список путёвок базового класса на расширенный.
        # Доступ через mangled-имя _travel_list оправдан: базовый
        # класс хранит список как приватный атрибут, а расширение хочет
        # сохранить весь публичный API родителя нетронутым.
        self._travel_list = TravelListExt()
        self._travel_list._parent_library = self

        self._airline_list = AirlineList()
        self._tour_operator_list = TourOperatorList()
        self._manager_list = ManagerList()
        self._payment_list = PaymentList()

    def clear(self):
        super().clear()
        self._airline_list.clear()
        self._tour_operator_list.clear()
        self._manager_list.clear()
        self._payment_list.clear()

    # ---------- путёвки (override с дополнительными FK) ----------
    def create_travel(self, code, date='', quantity=0, discount=0,
                     airline_code=0, touroperator_code=0, manager_code=0):
        travel = self._travel_list.create_item(
            code, date, quantity, discount,
            airline_code, touroperator_code, manager_code)
        if travel:
            travel._library = self
        return travel

    def new_travel(self, date='', quantity=0, discount=0,
                  airline_code=0, touroperator_code=0, manager_code=0):
        travel = self._travel_list.new_item(
            date, quantity, discount,
            airline_code, touroperator_code, manager_code)
        if travel:
            travel._library = self
        return travel

    def remove_travel(self, value):
        """Удаляем путёвку и каскадно — связанный с ней платёж."""
        code = value if isinstance(value, int) else value.get_code()
        super().remove_travel(value)
        pay = self._payment_list.find_by_package(code)
        if pay is not None:
            self._payment_list.remove_item(pay)

    # ---------- авиаперевозчики ----------
    def create_airline(self, code, name='', flight_cost=0):
        return self._airline_list.create_item(code, name, flight_cost)

    def new_airline(self, name='', flight_cost=0):
        return self._airline_list.new_item(name, flight_cost)

    def remove_airline(self, value):
        code = value if isinstance(value, int) else value.get_code()
        for p in self.get_travel_list():
            if hasattr(p, 'get_airline_code') and p.get_airline_code() == code:
                p.set_airline_code(0)
        self._airline_list.remove_item(value)

    def get_airline(self, code):
        return self._airline_list.find_by_code(code)

    def get_airline_list(self):
        return self._airline_list.get_items()

    def get_airline_new_code(self):
        return self._airline_list.get_new_code()

    # ---------- туроператоры ----------
    def create_tour_operator(self, code, name='', address='', phone='', website=''):
        return self._tour_operator_list.create_item(code, name, address, phone, website)

    def new_tour_operator(self, name='', address='', phone='', website=''):
        return self._tour_operator_list.new_item(name, address, phone, website)

    def remove_tour_operator(self, value):
        code = value if isinstance(value, int) else value.get_code()
        for p in self.get_travel_list():
            if hasattr(p, 'get_tour_operator_code') and p.get_tour_operator_code() == code:
                p.set_tour_operator_code(0)
        self._tour_operator_list.remove_item(value)

    def get_tour_operator(self, code):
        return self._tour_operator_list.find_by_code(code)

    def get_tour_operator_list(self):
        return self._tour_operator_list.get_items()

    def get_tour_operator_new_code(self):
        return self._tour_operator_list.get_new_code()

    # ---------- менеджеры ----------
    def create_manager(self, code, surname='', name='', secname='',
                      position='', phone='', email=''):
        return self._manager_list.create_item(code, surname, name, secname,
                                             position, phone, email)

    def new_manager(self, surname='', name='', secname='',
                   position='', phone='', email=''):
        return self._manager_list.new_item(surname, name, secname,
                                          position, phone, email)

    def remove_manager(self, value):
        code = value if isinstance(value, int) else value.get_code()
        for p in self.get_travel_list():
            if hasattr(p, 'get_manager_code') and p.get_manager_code() == code:
                p.set_manager_code(0)
        self._manager_list.remove_item(value)

    def get_manager(self, code):
        return self._manager_list.find_by_code(code)

    def get_manager_list(self):
        return self._manager_list.get_items()

    def get_manager_new_code(self):
        return self._manager_list.get_new_code()

    # ---------- платежи ----------
    def create_payment(self, code, package_code=0, date='', amount=0,
                      method='', status='в ожидании'):
        # Проверяем 1:1 связь — один платёж на путёвку
        existing = self._payment_list.find_by_package(int(package_code or 0))
        if existing is not None and existing.get_code() != code:
            raise ValueError(
                f'У путёвки {package_code} уже есть платёж {existing.get_code()} '
                f'(связь 1:1).')
        return self._payment_list.create_item(code, package_code, date, amount,
                                             method, status)

    def new_payment(self, package_code=0, date='', amount=0,
                   method='', status='в ожидании'):
        existing = self._payment_list.find_by_package(int(package_code or 0))
        if existing is not None:
            raise ValueError(
                f'У путёвки {package_code} уже есть платёж {existing.get_code()} '
                f'(связь 1:1).')
        return self._payment_list.new_item(package_code, date, amount,
                                          method, status)

    def remove_payment(self, value):
        self._payment_list.remove_item(value)

    def get_payment(self, code):
        return self._payment_list.find_by_code(code)

    def get_payment_by_package(self, package_code):
        return self._payment_list.find_by_package(package_code)

    def get_payment_list(self):
        return self._payment_list.get_items()

    def get_payment_codes(self):
        """Коды всех платежей (аналогично ``get_client_codes`` / ``get_travel_codes``)."""
        return self._payment_list.get_codes()

    def get_payment_new_code(self):
        return self._payment_list.get_new_code()
