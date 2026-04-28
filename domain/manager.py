"""Менеджер — сотрудник фирмы, оформивший путёвку."""

from domain.namedentity import namedentity


class manager(namedentity):
    """Сотрудник турфирмы: ФИО, должность, контакты.

    Поле ``name`` базового класса хранит имя; ``surname`` и ``secname``
    добавлены отдельно для полного ФИО.
    """

    def __init__(self, code=0, surname='', name='', secname='',
                 position='', phone='', email=''):
        super().__init__(code, name)
        self.setSurname(surname)
        self.setSecname(secname)
        self.setPosition(position)
        self.setPhone(phone)
        self.setEmail(email)

    def setSurname(self, value):
        self.__surname = value

    def setSecname(self, value):
        self.__secname = value

    def setPosition(self, value):
        self.__position = value

    def setPhone(self, value):
        self.__phone = value

    def setEmail(self, value):
        self.__email = value

    def getSurname(self):
        return self.__surname

    def getSecname(self):
        return self.__secname

    def getPosition(self):
        return self.__position

    def getPhone(self):
        return self.__phone

    def getEmail(self):
        return self.__email

    def getFullName(self):
        """Полное ФИО одной строкой."""
        parts = [self.getSurname(), self.getName(), self.getSecname()]
        return ' '.join(p for p in parts if p)
