import json
from dataaccess.data import data

class datajson(data):

    def getData(self):
        return self.__data

    def read(self):
        with open(self.getInp(), 'r', encoding='utf-8') as read_file:
            self.__data = json.load(read_file)
        self.readLists()

    def write(self):
        self.__data = {}
        self.writeLists()
        with open(self.getOut(), 'w', encoding='utf-8') as write_file:
            json.dump(self.__data, write_file, indent=2, ensure_ascii=False)

    def readClients(self):
        if 'clients' in self.getData().keys():
            for a in self.getData()['clients']:
                code, surname, name, secname, address, phone = (0, '', '', '', '', '')
                for ak in a.keys():
                    if ak == 'code':
                        code = a[ak]
                    if ak == 'surname':
                        surname = a[ak]
                    if ak == 'name':
                        name = a[ak]
                    if ak == 'secname':
                        secname = a[ak]
                    if ak == 'address':
                        address = a[ak]
                    if ak == 'phone':
                        phone = a[ak]
                self.getLib().createClient(code, surname, name, secname, address, phone)

    def readRoutes(self):
        if 'routes' in self.getData().keys():
            for a in self.getData()['routes']:
                code, name, climate, duration, hotel, cost = (0, '', '', 0, '', 0)
                for ak in a.keys():
                    if ak == 'code':
                        code = a[ak]
                    if ak == 'name':
                        name = a[ak]
                    if ak == 'climate':
                        climate = a[ak]
                    if ak == 'duration':
                        duration = a[ak]
                    if ak == 'hotel':
                        hotel = a[ak]
                    if ak == 'cost':
                        cost = a[ak]
                self.getLib().createRoute(code, name, climate, duration, hotel, cost)

    def readTravels(self):
        if 'travels' not in self.getData():
            return
        for a in self.getData()['travels']:
            code = a.get('code', 0)
            date = a.get('date', '')
            quantity = a.get('quantity', 0)
            discount = a.get('discount', 0)
            clients = a.get('clients', [])
            routes = a.get('routes', [])
            try:
                travel = self.getLib().createTravel(code, date, quantity, discount)
            except Exception as e:
                print(f'Ошибка создания путёвки {code}: {e}')
                continue
            if travel is None:
                print(f'Путёвка с кодом {code} не создана')
                continue
            for c in clients:
                if c is None:
                    continue
                try:
                    client_obj = self.getLib().getClient(c)
                    if client_obj is not None:
                        travel.appendClient(client_obj)
                    else:
                        print(f'Пропущен клиент {c} в путёвке {code} (не найден)')
                except Exception as e:
                    print(f'Ошибка добавления клиента {c} в путёвку {code}: {e}')
            for r in routes:
                if r is None:
                    continue
                try:
                    route_obj = self.getLib().getRoute(r)
                    if route_obj is not None:
                        travel.appendRoute(route_obj)
                    else:
                        print(f'Пропущен маршрут {r} в путёвке {code} (не найден)')
                except Exception as e:
                    print(f'Ошибка добавления маршрута {r} в путёвку {code}: {e}')

    def readLists(self):
        self.readClients()
        self.readRoutes()
        self.readTravels()

    def writeClients(self):
        self.getData()['clients'] = []
        for a in self.getLib().getClientList():
            ad = {}
            ad['code'] = a.getCode()
            ad['surname'] = a.getSurname()
            ad['name'] = a.getName()
            ad['secname'] = a.getSecname()
            ad['address'] = a.getAddress()
            ad['phone'] = a.getPhone()
            self.getData()['clients'].append(ad)

    def writeRoutes(self):
        self.getData()['routes'] = []
        for r in self.getLib().getRouteList():
            rd = {}
            rd['code'] = r.getCode()
            rd['name'] = r.getName()
            rd['climate'] = r.getClimate()
            rd['duration'] = r.getDuration()
            rd['hotel'] = r.getHotel()
            rd['cost'] = r.getCost()
            self.getData()['routes'].append(rd)

    def writeTravels(self):
        self.getData()['travels'] = []
        for t in self.getLib().getTravelList():
            td = {}
            td['code'] = t.getCode()
            td['date'] = t.getDate()
            td['quantity'] = t.getQuantity()
            td['discount'] = t.getDiscount()
            td['clients'] = t.getClientCodes()
            td['routes'] = t.getRouteCodes()
            self.getData()['travels'].append(td)

    def writeLists(self):
        self.writeClients()
        self.writeRoutes()
        self.writeTravels()
