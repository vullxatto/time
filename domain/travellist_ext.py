from domain.travellist import travelList
from domain.package_ext import package_ext

class travelList_ext(travelList):

    def createItem(self, code, date='', quantity=0, discount=0, airline_code=0, touroperator_code=0):
        if code in self.getCodes():
            print(f'Путёвка с кодом {code} уже существует')
            return None
        p = package_ext(code, date, quantity, discount, airline_code, touroperator_code)
        p._library = getattr(self, '_parent_library', None)
        super(travelList_ext, self).appendItem(p)
        return p

    def newItem(self, date='', quantity=0, discount=0, airline_code=0, touroperator_code=0):
        p = package_ext(self.getNewCode(), date, quantity, discount, airline_code, touroperator_code)
        p._library = getattr(self, '_parent_library', None)
        super(travelList_ext, self).appendItem(p)
        return p
