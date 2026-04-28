"""Путёвка — основная транзакционная сущность фирмы.

Путёвка связана с клиентами и маршрутами по принципу «многие ко многим»:
одна путёвка может включать нескольких клиентов и несколько маршрутов
(например, многодневный комбинированный тур по двум странам).
"""

from domain.entity import entity


class package(entity):
    """Купленная клиентом путёвка: дата, количество, скидка, клиенты, маршруты."""

    def __init__(self, code=0, date='', quantity=0, discount=0):
        super().__init__(code)
        self.setDate(date)
        self.setQuantity(quantity)
        self.setDiscount(discount)
        self.__clients = []
        self.__routes = []

    # --- скалярные атрибуты ---
    def setDate(self, value):
        self.__date = value

    def setQuantity(self, value):
        self.__quantity = value

    def setDiscount(self, value):
        self.__discount = value

    def getDate(self):
        return self.__date

    def getQuantity(self):
        return self.__quantity

    def getDiscount(self):
        return self.__discount

    # --- клиенты ---
    def appendClient(self, value):
        """Добавляет клиента: можно передать объект или код.

        При передаче кода требуется, чтобы у путёвки был установлен атрибут
        ``_library`` со ссылкой на ``TravelCompany`` — он используется для
        разрешения кода в объект клиента.
        """
        client_obj = self._resolve(value, 'getClient')
        if client_obj is not None and client_obj not in self.__clients:
            self.__clients.append(client_obj)

    def removeClient(self, value):
        if isinstance(value, int):
            for cl in self.__clients[:]:
                if cl.getCode() == value:
                    self.__clients.remove(cl)
                    return
        elif value in self.__clients:
            self.__clients.remove(value)

    def getClientCodes(self):
        return [c.getCode() for c in self.__clients]

    # --- маршруты ---
    def appendRoute(self, value):
        """Добавляет маршрут (объект или код); см. ``appendClient``."""
        route_obj = self._resolve(value, 'getRoute')
        if route_obj is not None and route_obj not in self.__routes:
            self.__routes.append(route_obj)

    def removeRoute(self, value):
        if isinstance(value, int):
            for rt in self.__routes[:]:
                if rt.getCode() == value:
                    self.__routes.remove(rt)
                    return
        elif value in self.__routes:
            self.__routes.remove(value)

    def getRouteCodes(self):
        return [r.getCode() for r in self.__routes]

    # --- helpers ---
    def _resolve(self, value, library_method):
        """Возвращает объект сущности по коду или сам объект, если он передан.

        ``library_method`` — имя метода у ``self._library`` для поиска по коду
        (``'getClient'`` или ``'getRoute'``).
        """
        if isinstance(value, int):
            lib = getattr(self, '_library', None)
            if lib is None:
                return None
            return getattr(lib, library_method)(value)
        if hasattr(value, 'getCode'):
            return value
        return None
