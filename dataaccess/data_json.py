"""Чтение/запись данных в JSON (3 базовые сущности)."""

import json
from dataaccess.data import Data


class DataJson(Data):

    def get_data(self):
        return self.__data

    def read(self):
        with open(self.get_inp(), 'r', encoding='utf-8') as f:
            self.__data = json.load(f)
        self.read_lists()

    def write(self):
        self.__data = {}
        self.write_lists()
        with open(self.get_out(), 'w', encoding='utf-8') as f:
            json.dump(self.__data, f, indent=2, ensure_ascii=False)

    def read_clients(self):
        for a in self.get_data().get('clients', []):
            self.get_lib().create_client(
                a.get('code', 0),
                a.get('surname', ''),
                a.get('name', ''),
                a.get('secname', ''),
                a.get('address', ''),
                a.get('phone', ''),
            )

    def read_routes(self):
        for a in self.get_data().get('routes', []):
            self.get_lib().create_route(
                a.get('code', 0),
                a.get('name', ''),
                a.get('climate', ''),
                a.get('duration', 0),
                a.get('hotel', ''),
                a.get('cost', 0),
            )

    def bind_travel_links(self, travel, record):
        """Связывает путёвку с клиентами и маршрутами из записи JSON.

        Коды разрешаются через ``package.append_client`` / ``append_route`` (нужен
        ``_library`` у путёвки).
        """
        for c in record.get('clients', []) or []:
            if c is None:
                continue
            travel.append_client(c)
        for r in record.get('routes', []) or []:
            if r is None:
                continue
            travel.append_route(r)

    def read_travels(self):
        for a in self.get_data().get('travels', []):
            code = a.get('code', 0)
            travel = self.get_lib().create_travel(
                code, a.get('date', ''), a.get('quantity', 0), a.get('discount', 0)
            )
            if travel is None:
                continue
            self.bind_travel_links(travel, a)

    def read_lists(self):
        self.read_clients()
        self.read_routes()
        self.read_travels()

    def write_clients(self):
        self.get_data()['clients'] = [
            {
                'code': c.get_code(),
                'surname': c.get_surname(),
                'name': c.get_name(),
                'secname': c.get_secname(),
                'address': c.get_address(),
                'phone': c.get_phone(),
            }
            for c in self.get_lib().get_client_list()
        ]

    def write_routes(self):
        self.get_data()['routes'] = [
            {
                'code': r.get_code(),
                'name': r.get_name(),
                'climate': r.get_climate(),
                'duration': r.get_duration(),
                'hotel': r.get_hotel(),
                'cost': r.get_cost(),
            }
            for r in self.get_lib().get_route_list()
        ]

    def write_travels(self):
        self.get_data()['travels'] = [
            {
                'code': t.get_code(),
                'date': t.get_date(),
                'quantity': t.get_quantity(),
                'discount': t.get_discount(),
                'clients': t.get_client_codes(),
                'routes': t.get_route_codes(),
            }
            for t in self.get_lib().get_travel_list()
        ]

    def write_lists(self):
        self.write_clients()
        self.write_routes()
        self.write_travels()
