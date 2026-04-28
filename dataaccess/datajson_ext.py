import json
from datajson import datajson

class datajson_ext(datajson):

    def read(self):
        super().read()
        self.readAirlines()
        self.readTourOperators()

    def write(self):
        setattr(self, '_datajson__data', {})
        self.writeLists()
        self.writeAirlines()
        self.writeTourOperators()
        with open(self.getOut(), 'w', encoding='utf-8') as f:
            json.dump(self.getData(), f, indent=2, ensure_ascii=False)

    def readTravels(self):
        if 'travels' not in self.getData():
            return
        for a in self.getData()['travels']:
            code = a.get('code', 0)
            date = a.get('date', '')
            quantity = a.get('quantity', 0)
            discount = a.get('discount', 0)
            airline_code = a.get('airline_code', 0) or 0
            touroperator_code = a.get('touroperator_code', 0) or 0
            clients = a.get('clients', [])
            routes = a.get('routes', [])
            try:
                travel = self.getLib().createTravel(code, date, quantity, discount, int(airline_code), int(touroperator_code))
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

    def readAirlines(self):
        if 'airlines' in self.getData():
            for a in self.getData()['airlines']:
                fc = a.get('flight_cost')
                if fc is None:
                    c = a.get('country', '')
                    try:
                        fc = int(c) if str(c).strip().isdigit() else 0
                    except (TypeError, ValueError):
                        fc = 0
                self.getLib().createAirline(a.get('code', 0), a.get('name', ''), int(fc) if fc is not None else 0)

    def readTourOperators(self):
        if 'touroperators' in self.getData():
            for t in self.getData()['touroperators']:
                self.getLib().createTourOperator(t.get('code', 0), t.get('name', ''), t.get('address', ''), t.get('phone', ''), t.get('website', ''))

    def writeAirlines(self):
        self.getData()['airlines'] = []
        for a in self.getLib().getAirlineList():
            self.getData()['airlines'].append({'code': a.getCode(), 'name': a.getName(), 'flight_cost': a.getFlightCost()})

    def writeTravels(self):
        self.getData()['travels'] = []
        for t in self.getLib().getTravelList():
            td = {'code': t.getCode(), 'date': t.getDate(), 'quantity': t.getQuantity(), 'discount': t.getDiscount(), 'clients': t.getClientCodes(), 'routes': t.getRouteCodes()}
            if hasattr(t, 'getAirlineCode'):
                td['airline_code'] = t.getAirlineCode()
                td['touroperator_code'] = t.getTourOperatorCode()
            else:
                td['airline_code'] = 0
                td['touroperator_code'] = 0
            self.getData()['travels'].append(td)

    def writeTourOperators(self):
        self.getData()['touroperators'] = []
        for t in self.getLib().getTourOperatorList():
            self.getData()['touroperators'].append({'code': t.getCode(), 'name': t.getName(), 'address': t.getAddress(), 'phone': t.getPhone(), 'website': t.getWebsite()})
