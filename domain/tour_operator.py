"""Туроператор — компания, организующая туры."""

from domain.named_entity import NamedEntity


class TourOperator(NamedEntity):
    """Компания-туроператор: адрес, телефон, сайт."""

    def __init__(self, code=0, name='', address='', phone='', website=''):
        super().__init__(code, name)
        self.set_address(address)
        self.set_phone(phone)
        self.set_website(website)

    def set_address(self, value):
        self.__address = value

    def set_phone(self, value):
        self.__phone = value

    def set_website(self, value):
        self.__website = value

    def get_address(self):
        return self.__address

    def get_phone(self):
        return self.__phone

    def get_website(self):
        return self.__website
