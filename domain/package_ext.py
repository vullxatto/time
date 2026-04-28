"""Расширенная путёвка: добавлены ссылки на авиаперевозчика, туроператора и менеджера.

Реализована через наследование от ``package`` — базовый класс инкапсулирует
саму сущность путёвки, а ``package_ext`` дополняет её FK-полями для связей
с контрагентами.
"""

from domain.package import package


class package_ext(package):
    """Путёвка с дополнительными FK-полями."""

    def __init__(self, code=0, date='', quantity=0, discount=0,
                 airline_code=0, touroperator_code=0, manager_code=0):
        super().__init__(code, date, quantity, discount)
        self.setAirlineCode(airline_code)
        self.setTourOperatorCode(touroperator_code)
        self.setManagerCode(manager_code)

    @staticmethod
    def _to_int(value):
        try:
            return int(value or 0)
        except (TypeError, ValueError):
            return 0

    def setAirlineCode(self, value):
        self.__airline_code = self._to_int(value)

    def getAirlineCode(self):
        return self.__airline_code

    def setTourOperatorCode(self, value):
        self.__touroperator_code = self._to_int(value)

    def getTourOperatorCode(self):
        return self.__touroperator_code

    def setManagerCode(self, value):
        self.__manager_code = self._to_int(value)

    def getManagerCode(self):
        return self.__manager_code
