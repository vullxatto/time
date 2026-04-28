"""Клиент туристической фирмы."""

from domain.namedentity import namedentity


class client(namedentity):
    """Физическое лицо, покупающее путёвки."""

    def __init__(self, code=0, surname='', name='', secname='', address='', phone=''):
        super().__init__(code, name)
        self.setSurname(surname)
        self.setSecname(secname)
        self.setAddress(address)
        self.setPhone(phone)

    def setSurname(self, value):
        self.__surname = value

    def setSecname(self, value):
        self.__secname = value

    def setAddress(self, value):
        self.__address = value

    def setPhone(self, value):
        self.__phone = value

    def getSurname(self):
        return self.__surname

    def getSecname(self):
        return self.__secname

    def getAddress(self):
        return self.__address

    def getPhone(self):
        return self.__phone

    def getClientInfo(self):
        return f'{self.getSurname()} {self.getName()} {self.getSecname()} {self.getAddress()} {self.getPhone()}'
