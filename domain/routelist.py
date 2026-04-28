from domain.entitylist import entityList
from domain.route import route

class routeList(entityList):

    def appendItem(self, value):
        if isinstance(value, route):
            super().appendItem(value)

    def createItem(self, code, name='', climate='', duration=0, hotel='', cost=0):
        if code in self.getCodes():
            print(f'Маршрут с кодом {code} уже существует')
        else:
            r = route(code, name, climate, duration, hotel, cost)
            super().appendItem(r)
            return r

    def newItem(self, name='', climate='', duration=0, hotel='', cost=0):
        r = route(self.getNewCode(), name, climate, duration, hotel, cost)
        super().appendItem(r)
        return r
