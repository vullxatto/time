"""Расширенная модель турфирмы.

Базовый ``TravelCompany`` отвечает за три ключевые сущности предметной области
(клиенты, маршруты, путёвки). Подкласс ``TravelCompany_ext`` дополняет модель
ещё четырьмя через наследование, не затрагивая базовый API:

  - авиаперевозчики (FK 1:N от путёвки)
  - туроператоры    (FK 1:N от путёвки)
  - менеджеры       (FK 1:N от путёвки)
  - платежи         (1:1 к путёвке через FK package_code)
"""

from domain.TravelCompany import TravelCompany
from domain.travellist_ext import travelList_ext
from domain.airlinelist import airlineList
from domain.touroperatorlist import touroperatorList
from domain.managerlist import managerList
from domain.paymentlist import paymentList


class TravelCompany_ext(TravelCompany):

    def __init__(self):
        super().__init__()
        # Подменяем приватный список путёвок базового класса на расширенный.
        # Доступ через mangled-имя _TravelCompany__travelList оправдан: базовый
        # класс хранит список как приватный атрибут, а расширение хочет
        # сохранить весь публичный API родителя нетронутым.
        self._TravelCompany__travelList = travelList_ext()
        self._TravelCompany__travelList._parent_library = self

        self.__airlineList = airlineList()
        self.__touroperatorList = touroperatorList()
        self.__managerList = managerList()
        self.__paymentList = paymentList()

    def clear(self):
        super().clear()
        self.__airlineList.clear()
        self.__touroperatorList.clear()
        self.__managerList.clear()
        self.__paymentList.clear()

    # ---------- путёвки (override с дополнительными FK) ----------
    def createTravel(self, code, date='', quantity=0, discount=0,
                     airline_code=0, touroperator_code=0, manager_code=0):
        travel = self._TravelCompany__travelList.createItem(
            code, date, quantity, discount,
            airline_code, touroperator_code, manager_code)
        if travel:
            travel._library = self
        return travel

    def newTravel(self, date='', quantity=0, discount=0,
                  airline_code=0, touroperator_code=0, manager_code=0):
        travel = self._TravelCompany__travelList.newItem(
            date, quantity, discount,
            airline_code, touroperator_code, manager_code)
        if travel:
            travel._library = self
        return travel

    def removeTravel(self, value):
        """Удаляем путёвку и каскадно — связанный с ней платёж."""
        code = value if isinstance(value, int) else value.getCode()
        super().removeTravel(value)
        pay = self.__paymentList.findByPackage(code)
        if pay is not None:
            self.__paymentList.removeItem(pay)

    # ---------- авиаперевозчики ----------
    def createAirline(self, code, name='', flight_cost=0):
        return self.__airlineList.createItem(code, name, flight_cost)

    def newAirline(self, name='', flight_cost=0):
        return self.__airlineList.newItem(name, flight_cost)

    def removeAirline(self, value):
        code = value if isinstance(value, int) else value.getCode()
        for p in self.getTravelList():
            if hasattr(p, 'getAirlineCode') and p.getAirlineCode() == code:
                p.setAirlineCode(0)
        self.__airlineList.removeItem(value)

    def getAirline(self, code):
        return self.__airlineList.findByCode(code)

    def getAirlineList(self):
        return self.__airlineList.getItems()

    def getAirlineNewCode(self):
        return self.__airlineList.getNewCode()

    # ---------- туроператоры ----------
    def createTourOperator(self, code, name='', address='', phone='', website=''):
        return self.__touroperatorList.createItem(code, name, address, phone, website)

    def newTourOperator(self, name='', address='', phone='', website=''):
        return self.__touroperatorList.newItem(name, address, phone, website)

    def removeTourOperator(self, value):
        code = value if isinstance(value, int) else value.getCode()
        for p in self.getTravelList():
            if hasattr(p, 'getTourOperatorCode') and p.getTourOperatorCode() == code:
                p.setTourOperatorCode(0)
        self.__touroperatorList.removeItem(value)

    def getTourOperator(self, code):
        return self.__touroperatorList.findByCode(code)

    def getTourOperatorList(self):
        return self.__touroperatorList.getItems()

    def getTourOperatorNewCode(self):
        return self.__touroperatorList.getNewCode()

    # ---------- менеджеры ----------
    def createManager(self, code, surname='', name='', secname='',
                      position='', phone='', email=''):
        return self.__managerList.createItem(code, surname, name, secname,
                                             position, phone, email)

    def newManager(self, surname='', name='', secname='',
                   position='', phone='', email=''):
        return self.__managerList.newItem(surname, name, secname,
                                          position, phone, email)

    def removeManager(self, value):
        code = value if isinstance(value, int) else value.getCode()
        for p in self.getTravelList():
            if hasattr(p, 'getManagerCode') and p.getManagerCode() == code:
                p.setManagerCode(0)
        self.__managerList.removeItem(value)

    def getManager(self, code):
        return self.__managerList.findByCode(code)

    def getManagerList(self):
        return self.__managerList.getItems()

    def getManagerNewCode(self):
        return self.__managerList.getNewCode()

    # ---------- платежи ----------
    def createPayment(self, code, package_code=0, date='', amount=0,
                      method='', status='в ожидании'):
        # Проверяем 1:1 связь — один платёж на путёвку
        existing = self.__paymentList.findByPackage(int(package_code or 0))
        if existing is not None and existing.getCode() != code:
            print(f'У путёвки {package_code} уже есть платёж '
                  f'{existing.getCode()} (связь 1:1)')
            return None
        return self.__paymentList.createItem(code, package_code, date, amount,
                                             method, status)

    def newPayment(self, package_code=0, date='', amount=0,
                   method='', status='в ожидании'):
        existing = self.__paymentList.findByPackage(int(package_code or 0))
        if existing is not None:
            print(f'У путёвки {package_code} уже есть платёж '
                  f'{existing.getCode()} (связь 1:1)')
            return None
        return self.__paymentList.newItem(package_code, date, amount,
                                          method, status)

    def removePayment(self, value):
        self.__paymentList.removeItem(value)

    def getPayment(self, code):
        return self.__paymentList.findByCode(code)

    def getPaymentByPackage(self, package_code):
        return self.__paymentList.findByPackage(package_code)

    def getPaymentList(self):
        return self.__paymentList.getItems()

    def getPaymentNewCode(self):
        return self.__paymentList.getNewCode()
