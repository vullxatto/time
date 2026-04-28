"""Туроператор — компания, организующая туры."""

from domain.namedentity import namedentity


class touroperator(namedentity):
    """Компания-туроператор: адрес, телефон, сайт."""

    def __init__(self, code=0, name='', address='', phone='', website=''):
        super().__init__(code, name)
        self.setAddress(address)
        self.setPhone(phone)
        self.setWebsite(website)

    def setAddress(self, value):
        self.__address = value

    def setPhone(self, value):
        self.__phone = value

    def setWebsite(self, value):
        self.__website = value

    def getAddress(self):
        return self.__address

    def getPhone(self):
        return self.__phone

    def getWebsite(self):
        return self.__website
