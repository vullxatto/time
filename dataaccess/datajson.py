"""Чтение/запись данных в JSON (3 базовые сущности)."""

import json
from dataaccess.data import data


class datajson(data):

    def getData(self):
        return self.__data

    def read(self):
        with open(self.getInp(), 'r', encoding='utf-8') as f:
            self.__data = json.load(f)
        self.readLists()

    def write(self):
        self.__data = {}
        self.writeLists()
        with open(self.getOut(), 'w', encoding='utf-8') as f:
            json.dump(self.__data, f, indent=2, ensure_ascii=False)

    def readClients(self):
        for a in self.getData().get('clients', []):
            self.getLib().createClient(
                a.get('code', 0),
                a.get('surname', ''),
                a.get('name', ''),
                a.get('secname', ''),
                a.get('address', ''),
                a.get('phone', ''),
            )

    def readRoutes(self):
        for a in self.getData().get('routes', []):
            self.getLib().createRoute(
                a.get('code', 0),
                a.get('name', ''),
                a.get('climate', ''),
                a.get('duration', 0),
                a.get('hotel', ''),
                a.get('cost', 0),
            )

    def readTravels(self):
        for a in self.getData().get('travels', []):
            code = a.get('code', 0)
            travel = self.getLib().createTravel(
                code, a.get('date', ''), a.get('quantity', 0), a.get('discount', 0)
            )
            if travel is None:
                continue
            for c in a.get('clients', []) or []:
                if c is None:
                    continue
                obj = self.getLib().getClient(c)
                if obj is not None:
                    travel.appendClient(obj)
            for r in a.get('routes', []) or []:
                if r is None:
                    continue
                obj = self.getLib().getRoute(r)
                if obj is not None:
                    travel.appendRoute(obj)

    def readLists(self):
        self.readClients()
        self.readRoutes()
        self.readTravels()

    def writeClients(self):
        self.getData()['clients'] = [
            {
                'code': c.getCode(),
                'surname': c.getSurname(),
                'name': c.getName(),
                'secname': c.getSecname(),
                'address': c.getAddress(),
                'phone': c.getPhone(),
            }
            for c in self.getLib().getClientList()
        ]

    def writeRoutes(self):
        self.getData()['routes'] = [
            {
                'code': r.getCode(),
                'name': r.getName(),
                'climate': r.getClimate(),
                'duration': r.getDuration(),
                'hotel': r.getHotel(),
                'cost': r.getCost(),
            }
            for r in self.getLib().getRouteList()
        ]

    def writeTravels(self):
        self.getData()['travels'] = [
            {
                'code': t.getCode(),
                'date': t.getDate(),
                'quantity': t.getQuantity(),
                'discount': t.getDiscount(),
                'clients': t.getClientCodes(),
                'routes': t.getRouteCodes(),
            }
            for t in self.getLib().getTravelList()
        ]

    def writeLists(self):
        self.writeClients()
        self.writeRoutes()
        self.writeTravels()
