"""Путёвка — основная транзакционная сущность фирмы.

Путёвка связана с клиентами и маршрутами по принципу «многие ко многим»:
одна путёвка может включать нескольких клиентов и несколько маршрутов
(например, многодневный комбинированный тур по двум странам).
"""

from domain.entity import Entity


class Package(Entity):
    """Купленная клиентом путёвка: дата, количество, скидка, клиенты, маршруты."""

    def __init__(self, code=0, date='', quantity=0, discount=0):
        super().__init__(code)
        self.set_date(date)
        self.set_quantity(quantity)
        self.set_discount(discount)
        self.__clients = []
        self.__routes = []

    # --- скалярные атрибуты ---
    def set_date(self, value):
        self.__date = value

    def set_quantity(self, value):
        self.__quantity = value

    def set_discount(self, value):
        self.__discount = value

    def get_date(self):
        return self.__date

    def get_quantity(self):
        return self.__quantity

    def get_discount(self):
        return self.__discount

    # --- клиенты ---
    def append_client(self, value):
        """Добавляет клиента: можно передать объект или код.

        При передаче кода требуется, чтобы у путёвки был установлен атрибут
        ``_library`` со ссылкой на ``TravelCompany`` — он используется для
        разрешения кода в объект клиента.
        """
        client_obj = self._resolve(value, 'get_client')
        if client_obj is not None and client_obj not in self.__clients:
            self.__clients.append(client_obj)

    def remove_client(self, value):
        if isinstance(value, int):
            for cl in self.__clients[:]:
                if cl.get_code() == value:
                    self.__clients.remove(cl)
                    return
        elif value in self.__clients:
            self.__clients.remove(value)

    def get_client_codes(self):
        return [c.get_code() for c in self.__clients]

    # --- маршруты ---
    def append_route(self, value):
        """Добавляет маршрут (объект или код); см. ``append_client``."""
        route_obj = self._resolve(value, 'get_route')
        if route_obj is not None and route_obj not in self.__routes:
            self.__routes.append(route_obj)

    def remove_route(self, value):
        if isinstance(value, int):
            for rt in self.__routes[:]:
                if rt.get_code() == value:
                    self.__routes.remove(rt)
                    return
        elif value in self.__routes:
            self.__routes.remove(value)

    def get_route_codes(self):
        return [r.get_code() for r in self.__routes]

    # --- helpers ---
    def _resolve(self, value, library_method):
        """Возвращает объект сущности по коду или сам объект, если он передан.

        ``library_method`` — имя метода у ``self._library`` для поиска по коду
        (``'get_client'`` или ``'get_route'``).
        """
        if isinstance(value, int):
            lib = getattr(self, '_library', None)
            if lib is None:
                return None
            return getattr(lib, library_method)(value)
        if hasattr(value, 'get_code'):
            return value
        return None
