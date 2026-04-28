from domain.entity import entity

class package(entity):

    def __init__(self, code=0, date='', quantity=0, discount=0):
        super().__init__(code)
        self.setDate(date)
        self.setQuantity(quantity)
        self.setDiscount(discount)
        self.__clients = []
        self.__routes = []

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

    def appendClient(self, value):
        if isinstance(value, int):
            if hasattr(self, '_library') and self._library:
                client_obj = self._library.getClient(value)
                if client_obj and client_obj not in self.__clients:
                    self.__clients.append(client_obj)
            else:
                print(f'Warning: package.appendClient({value}) - нет доступа к library')
        elif hasattr(value, 'getCode') and value not in self.__clients:
            if value not in self.__clients:
                self.__clients.append(value)

    def removeClient(self, value):
        if isinstance(value, int):
            for cl in self.__clients[:]:
                if cl.getCode() == value:
                    self.__clients.remove(cl)
                    break
        elif value in self.__clients:
            self.__clients.remove(value)

    def getClientCodes(self):
        return [c.getCode() for c in self.__clients]

    def appendRoute(self, value):
        if isinstance(value, int):
            if hasattr(self, '_library') and self._library:
                route_obj = self._library.getRoute(value)
                if route_obj and route_obj not in self.__routes:
                    self.__routes.append(route_obj)
            else:
                print(f'Warning: package.appendRoute({value}) - нет доступа к library')
        elif hasattr(value, 'getCode') and value not in self.__routes:
            if value not in self.__routes:
                self.__routes.append(value)

    def removeRoute(self, value):
        if isinstance(value, int):
            for rt in self.__routes[:]:
                if rt.getCode() == value:
                    self.__routes.remove(rt)
                    break
        elif value in self.__routes:
            self.__routes.remove(value)

    def getRouteCodes(self):
        return [r.getCode() for r in self.__routes]
