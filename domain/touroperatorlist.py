from entitylist import entityList
from touroperator import touroperator

class touroperatorList(entityList):

    def appendItem(self, value):
        if isinstance(value, touroperator):
            super().appendItem(value)

    def createItem(self, code, name='', address='', phone='', website=''):
        if code in self.getCodes():
            print(f'Туроператор с кодом {code} уже существует')
        else:
            t = touroperator(code, name, address, phone, website)
            super().appendItem(t)
            return t

    def newItem(self, name='', address='', phone='', website=''):
        t = touroperator(self.getNewCode(), name, address, phone, website)
        super().appendItem(t)
        return t
