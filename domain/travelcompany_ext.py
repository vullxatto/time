from airlinelist import airlineList
from touroperatorlist import touroperatorList
from TravelCompany import TravelCompany
from domain.travellist_ext import travelList_ext

class TravelCompany_ext(TravelCompany):

    def __init__(self):
        super().__init__()
        self._TravelCompany__travelList = travelList_ext()
        self._TravelCompany__travelList._parent_library = self
        self.__airlineList = airlineList()
        self.__touroperatorList = touroperatorList()

    def clear(self):
        super().clear()
        self.__airlineList.clear()
        self.__touroperatorList.clear()

    def createTravel(self, code, date='', quantity=0, discount=0, airline_code=0, touroperator_code=0):
        travel = self._TravelCompany__travelList.createItem(code, date, quantity, discount, airline_code, touroperator_code)
        if travel:
            travel._library = self
        return travel

    def newTravel(self, date='', quantity=0, discount=0, airline_code=0, touroperator_code=0):
        travel = self._TravelCompany__travelList.newItem(date, quantity, discount, airline_code, touroperator_code)
        if travel:
            travel._library = self
        return travel

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
