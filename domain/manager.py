"""Менеджер — сотрудник фирмы, оформивший путёвку."""

from domain.named_entity import NamedEntity


class Manager(NamedEntity):
    """Сотрудник турфирмы: ФИО, должность, контакты.

    Поле ``name`` базового класса хранит имя; ``surname`` и ``secname``
    добавлены отдельно для полного ФИО.
    """

    def __init__(self, code=0, surname='', name='', secname='',
                 position='', phone='', email=''):
        super().__init__(code, name)
        self.set_surname(surname)
        self.set_secname(secname)
        self.set_position(position)
        self.set_phone(phone)
        self.set_email(email)

    def set_surname(self, value):
        self.__surname = value

    def set_secname(self, value):
        self.__secname = value

    def set_position(self, value):
        self.__position = value

    def set_phone(self, value):
        self.__phone = value

    def set_email(self, value):
        self.__email = value

    def get_surname(self):
        return self.__surname

    def get_secname(self):
        return self.__secname

    def get_position(self):
        return self.__position

    def get_phone(self):
        return self.__phone

    def get_email(self):
        return self.__email

    def get_full_name(self):
        """Полное ФИО одной строкой."""
        parts = [self.get_surname(), self.get_name(), self.get_secname()]
        return ' '.join(p for p in parts if p)
