"""Клиент туристической фирмы."""

from domain.entity import Entity


class Client(Entity):
    """Физическое лицо, покупающее путёвки (ФИО и контакты хранятся раздельно)."""

    def __init__(self, code=0, surname='', name='', secname='', address='', phone=''):
        super().__init__(code)
        self.set_surname(surname)
        self.set_name(name)
        self.set_secname(secname)
        self.set_address(address)
        self.set_phone(phone)

    def set_surname(self, value):
        self.__surname = value

    def set_name(self, value):
        self.__name = value

    def set_secname(self, value):
        self.__secname = value

    def set_address(self, value):
        self.__address = value

    def set_phone(self, value):
        self.__phone = value

    def get_surname(self):
        return self.__surname

    def get_name(self):
        return self.__name

    def get_secname(self):
        return self.__secname

    def get_address(self):
        return self.__address

    def get_phone(self):
        return self.__phone

    def get_client_info(self):
        return (
            f'{self.get_surname()} {self.get_name()} {self.get_secname()} '
            f'{self.get_address()} {self.get_phone()}'
        )
