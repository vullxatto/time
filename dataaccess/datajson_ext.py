"""Расширенный JSON-сериализатор: добавляет авиа, туроп, менеджеров, платежи."""

import json
from dataaccess.datajson import datajson


class datajson_ext(datajson):

    def read(self):
        super().read()
        self.readAirlines()
        self.readTourOperators()
        self.readManagers()
        self.readPayments()

    def write(self):
        # Перед записью обнуляем словарь данных родителя (он приватный), затем
        # последовательно вызываем все writeXxx и наконец сериализуем.
        setattr(self, '_datajson__data', {})
        self.writeLists()
        self.writeAirlines()
        self.writeTourOperators()
        self.writeManagers()
        self.writePayments()
        with open(self.getOut(), 'w', encoding='utf-8') as f:
            json.dump(self.getData(), f, indent=2, ensure_ascii=False)

    # ---------- путёвки (с FK на авиа/туроп/менеджера) ----------
    def readTravels(self):
        for a in self.getData().get('travels', []):
            code = a.get('code', 0)
            try:
                travel = self.getLib().createTravel(
                    code,
                    a.get('date', ''),
                    a.get('quantity', 0),
                    a.get('discount', 0),
                    int(a.get('airline_code', 0) or 0),
                    int(a.get('touroperator_code', 0) or 0),
                    int(a.get('manager_code', 0) or 0),
                )
            except Exception as e:
                print(f'Ошибка создания путёвки {code}: {e}')
                continue
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

    def writeTravels(self):
        self.getData()['travels'] = []
        for t in self.getLib().getTravelList():
            td = {
                'code': t.getCode(),
                'date': t.getDate(),
                'quantity': t.getQuantity(),
                'discount': t.getDiscount(),
                'clients': t.getClientCodes(),
                'routes': t.getRouteCodes(),
                'airline_code': t.getAirlineCode() if hasattr(t, 'getAirlineCode') else 0,
                'touroperator_code': t.getTourOperatorCode() if hasattr(t, 'getTourOperatorCode') else 0,
                'manager_code': t.getManagerCode() if hasattr(t, 'getManagerCode') else 0,
            }
            self.getData()['travels'].append(td)

    # ---------- авиаперевозчики ----------
    def readAirlines(self):
        for a in self.getData().get('airlines', []):
            fc = a.get('flight_cost', 0)
            try:
                fc = int(fc) if fc not in (None, '') else 0
            except (TypeError, ValueError):
                fc = 0
            self.getLib().createAirline(a.get('code', 0), a.get('name', ''), fc)

    def writeAirlines(self):
        self.getData()['airlines'] = [
            {'code': a.getCode(), 'name': a.getName(), 'flight_cost': a.getFlightCost()}
            for a in self.getLib().getAirlineList()
        ]

    # ---------- туроператоры ----------
    def readTourOperators(self):
        for t in self.getData().get('touroperators', []):
            self.getLib().createTourOperator(
                t.get('code', 0),
                t.get('name', ''),
                t.get('address', ''),
                t.get('phone', ''),
                t.get('website', ''),
            )

    def writeTourOperators(self):
        self.getData()['touroperators'] = [
            {
                'code': t.getCode(),
                'name': t.getName(),
                'address': t.getAddress(),
                'phone': t.getPhone(),
                'website': t.getWebsite(),
            }
            for t in self.getLib().getTourOperatorList()
        ]

    # ---------- менеджеры ----------
    def readManagers(self):
        for m in self.getData().get('managers', []):
            self.getLib().createManager(
                m.get('code', 0),
                m.get('surname', ''),
                m.get('name', ''),
                m.get('secname', ''),
                m.get('position', ''),
                m.get('phone', ''),
                m.get('email', ''),
            )

    def writeManagers(self):
        self.getData()['managers'] = [
            {
                'code': m.getCode(),
                'surname': m.getSurname(),
                'name': m.getName(),
                'secname': m.getSecname(),
                'position': m.getPosition(),
                'phone': m.getPhone(),
                'email': m.getEmail(),
            }
            for m in self.getLib().getManagerList()
        ]

    # ---------- платежи ----------
    def readPayments(self):
        for p in self.getData().get('payments', []):
            self.getLib().createPayment(
                p.get('code', 0),
                p.get('package_code', 0),
                p.get('date', ''),
                p.get('amount', 0),
                p.get('method', ''),
                p.get('status', 'в ожидании'),
            )

    def writePayments(self):
        self.getData()['payments'] = [
            {
                'code': p.getCode(),
                'package_code': p.getPackageCode(),
                'date': p.getDate(),
                'amount': p.getAmount(),
                'method': p.getMethod(),
                'status': p.getStatus(),
            }
            for p in self.getLib().getPaymentList()
        ]
