from domain.clientlist import clientList
from domain.routelist import routeList
from domain.travellist import travelList

class TravelCompany:

    def __init__(self):
        self.__clientList = clientList()
        self.__routeList = routeList()
        self.__travelList = travelList()
        self.__travelList._parent_library = self

    def clear(self):
        self.__clientList.clear()
        self.__routeList.clear()
        self.__travelList.clear()

    def createClient(self, code, surname='', name='', secname='', address='', phone=''):
        return self.__clientList.createItem(code, surname, name, secname, address, phone)

    def newClient(self, surname='', name='', secname='', address='', phone=''):
        return self.__clientList.newItem(surname, name, secname, address, phone)

    def removeClient(self, value):
        self.__clientList.removeItem(value)
        for p in self.__travelList.getItems():
            p.removeClient(value)

    def getClient(self, code):
        return self.__clientList.findByCode(code)

    def getClientList(self):
        return self.__clientList.getItems()

    def getClientCodes(self):
        return self.__clientList.getCodes()

    def getClientNewCode(self):
        return self.__clientList.getNewCode()

    def createRoute(self, code, name='', climate='', duration=0, hotel='', cost=0):
        return self.__routeList.createItem(code, name, climate, duration, hotel, cost)

    def newRoute(self, name='', climate='', duration=0, hotel='', cost=0):
        return self.__routeList.newItem(name, climate, duration, hotel, cost)

    def removeRoute(self, value):
        self.__routeList.removeItem(value)
        for p in self.__travelList.getItems():
            p.removeRoute(value)

    def getRoute(self, code):
        return self.__routeList.findByCode(code)

    def getRouteList(self):
        return self.__routeList.getItems()

    def getRouteCodes(self):
        return self.__routeList.getCodes()

    def getRouteNewCode(self):
        return self.__routeList.getNewCode()

    def createTravel(self, code, date='', quantity=0, discount=0):
        travel = self.__travelList.createItem(code, date, quantity, discount)
        if travel:
            travel._library = self
        return travel

    def newTravel(self, date='', quantity=0, discount=0):
        travel = self.__travelList.newItem(date, quantity, discount)
        if travel:
            travel._library = self
        return travel

    def removeTravel(self, value):
        self.__travelList.removeItem(value)

    def getTravel(self, code):
        return self.__travelList.findByCode(code)

    def getTravelList(self):
        return self.__travelList.getItems()

    def getTravelCodes(self):
        return self.__travelList.getCodes()

    def getTravelNewCode(self):
        return self.__travelList.getNewCode()
