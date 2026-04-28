"""Платёж за путёвку (финансовая сторона деятельности фирмы)."""

from domain.entity import entity


# Допустимые значения, используемые UI (для подсказок и проверок)
PAYMENT_METHODS = ('наличные', 'карта', 'перевод')
PAYMENT_STATUSES = ('оплачен', 'в ожидании', 'отменён')


class payment(entity):
    """Платёж: дата, сумма, способ оплаты, статус и ссылка на путёвку.

    Связь с путёвкой реализована через хранение её кода (``package_code``).
    Связь 1:1 поддерживается на уровне коллекции платежей и БД (UNIQUE).
    """

    def __init__(self, code=0, package_code=0, date='', amount=0,
                 method='', status='в ожидании'):
        super().__init__(code)
        self.setPackageCode(package_code)
        self.setDate(date)
        self.setAmount(amount)
        self.setMethod(method)
        self.setStatus(status)

    def setPackageCode(self, value):
        try:
            self.__package_code = int(value or 0)
        except (TypeError, ValueError):
            self.__package_code = 0

    def setDate(self, value):
        self.__date = value or ''

    def setAmount(self, value):
        try:
            self.__amount = int(value or 0)
        except (TypeError, ValueError):
            self.__amount = 0

    def setMethod(self, value):
        self.__method = value or ''

    def setStatus(self, value):
        self.__status = value or 'в ожидании'

    def getPackageCode(self):
        return self.__package_code

    def getDate(self):
        return self.__date

    def getAmount(self):
        return self.__amount

    def getMethod(self):
        return self.__method

    def getStatus(self):
        return self.__status

    def isPaid(self):
        return self.__status == 'оплачен'
