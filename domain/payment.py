"""Платёж за путёвку (финансовая сторона деятельности фирмы)."""

from domain.entity import Entity


# Допустимые значения, используемые UI (для подсказок и проверок)
PAYMENT_METHODS = ('наличные', 'карта', 'перевод')
PAYMENT_STATUSES = ('оплачен', 'в ожидании', 'отменён')


class Payment(Entity):
    """Платёж: дата, сумма, способ оплаты, статус и ссылка на путёвку.

    Связь с путёвкой реализована через хранение её кода (``package_code``).
    Связь 1:1 поддерживается на уровне коллекции платежей и БД (UNIQUE).
    """

    def __init__(self, code=0, package_code=0, date='', amount=0,
                 method='', status='в ожидании'):
        super().__init__(code)
        self.set_package_code(package_code)
        self.set_date(date)
        self.set_amount(amount)
        self.set_method(method)
        self.set_status(status)

    def set_package_code(self, value):
        try:
            self.__package_code = int(value or 0)
        except (TypeError, ValueError):
            self.__package_code = 0

    def set_date(self, value):
        self.__date = value or ''

    def set_amount(self, value):
        try:
            self.__amount = int(value or 0)
        except (TypeError, ValueError):
            self.__amount = 0

    def set_method(self, value):
        self.__method = value or ''

    def set_status(self, value):
        self.__status = value or 'в ожидании'

    def get_package_code(self):
        return self.__package_code

    def get_date(self):
        return self.__date

    def get_amount(self):
        return self.__amount

    def get_method(self):
        return self.__method

    def get_status(self):
        return self.__status

    def is_paid(self):
        return self.__status == 'оплачен'
