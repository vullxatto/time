from domain.entity import entity

class namedentity(entity):

    def __init__(self, code=0, name=''):
        super().__init__(code)
        self.setName(name)

    def setName(self, value):
        self.__name = value

    def getName(self):
        return self.__name
