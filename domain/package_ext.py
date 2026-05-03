"""Расширенная путёвка: добавлены ссылки на авиаперевозчика, туроператора и менеджера.

Реализована через наследование от ``package`` — базовый класс инкапсулирует
саму сущность путёвки, а ``PackageExt`` дополняет её FK-полями для связей
с контрагентами.
"""

from domain.package import Package
from domain.utils import to_int


class PackageExt(Package):
    """Путёвка с дополнительными FK-полями."""

    def __init__(self, code=0, date='', quantity=0, discount=0,
                 airline_code=0, touroperator_code=0, manager_code=0):
        super().__init__(code, date, quantity, discount)
        self.set_airline_code(airline_code)
        self.set_tour_operator_code(touroperator_code)
        self.set_manager_code(manager_code)

    def set_airline_code(self, value):
        self.__airline_code = to_int(value)

    def get_airline_code(self):
        return self.__airline_code

    def set_tour_operator_code(self, value):
        self.__touroperator_code = to_int(value)

    def get_tour_operator_code(self):
        return self.__touroperator_code

    def set_manager_code(self, value):
        self.__manager_code = to_int(value)

    def get_manager_code(self):
        return self.__manager_code
