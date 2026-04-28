from domain.package import package

class package_ext(package):

    def __init__(self, code=0, date='', quantity=0, discount=0, airline_code=0, touroperator_code=0):
        super().__init__(code, date, quantity, discount)
        self.setAirlineCode(airline_code)
        self.setTourOperatorCode(touroperator_code)

    def setAirlineCode(self, value):
        try:
            self.__airline_code = int(value or 0)
        except (TypeError, ValueError):
            self.__airline_code = 0

    def getAirlineCode(self):
        return self.__airline_code

    def setTourOperatorCode(self, value):
        try:
            self.__touroperator_code = int(value or 0)
        except (TypeError, ValueError):
            self.__touroperator_code = 0

    def getTourOperatorCode(self):
        return self.__touroperator_code
