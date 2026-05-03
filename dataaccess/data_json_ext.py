"""Расширенный JSON-сериализатор: добавляет авиа, туроп, менеджеров, платежи."""

import json
from dataaccess.data_json import DataJson


class DataJsonExt(DataJson):

    def read(self):
        super().read()
        self.read_airlines()
        self.read_tour_operators()
        self.read_managers()
        self.read_payments()

    def write(self):
        # Перед записью обнуляем словарь данных родителя (он приватный), затем
        # последовательно вызываем все writeXxx и наконец сериализуем.
        setattr(self, '_DataJson__data', {})
        self.write_lists()
        self.write_airlines()
        self.write_tour_operators()
        self.write_managers()
        self.write_payments()
        with open(self.get_out(), 'w', encoding='utf-8') as f:
            json.dump(self.get_data(), f, indent=2, ensure_ascii=False)

    # ---------- путёвки (с FK на авиа/туроп/менеджера) ----------
    def read_travels(self):
        for a in self.get_data().get('travels', []):
            code = a.get('code', 0)
            try:
                travel = self.get_lib().create_travel(
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
            self.bind_travel_links(travel, a)

    def write_travels(self):
        self.get_data()['travels'] = []
        for t in self.get_lib().get_travel_list():
            ac, oc, mc = self._travel_foreign_codes(t)
            td = {
                'code': t.get_code(),
                'date': t.get_date(),
                'quantity': t.get_quantity(),
                'discount': t.get_discount(),
                'clients': t.get_client_codes(),
                'routes': t.get_route_codes(),
                'airline_code': ac,
                'touroperator_code': oc,
                'manager_code': mc,
            }
            self.get_data()['travels'].append(td)

    @staticmethod
    def _travel_foreign_codes(t):
        """Коды FK для сериализации путёвки (базовый package без методов — нули)."""
        if hasattr(t, 'get_airline_code'):
            return (t.get_airline_code(), t.get_tour_operator_code(), t.get_manager_code())
        return (0, 0, 0)

    # ---------- авиаперевозчики ----------
    def read_airlines(self):
        for a in self.get_data().get('airlines', []):
            fc = a.get('flight_cost', 0)
            try:
                fc = int(fc) if fc not in (None, '') else 0
            except (TypeError, ValueError):
                fc = 0
            self.get_lib().create_airline(a.get('code', 0), a.get('name', ''), fc)

    def write_airlines(self):
        self.get_data()['airlines'] = [
            {'code': a.get_code(), 'name': a.get_name(), 'flight_cost': a.get_flight_cost()}
            for a in self.get_lib().get_airline_list()
        ]

    # ---------- туроператоры ----------
    def read_tour_operators(self):
        for t in self.get_data().get('touroperators', []):
            self.get_lib().create_tour_operator(
                t.get('code', 0),
                t.get('name', ''),
                t.get('address', ''),
                t.get('phone', ''),
                t.get('website', ''),
            )

    def write_tour_operators(self):
        self.get_data()['touroperators'] = [
            {
                'code': t.get_code(),
                'name': t.get_name(),
                'address': t.get_address(),
                'phone': t.get_phone(),
                'website': t.get_website(),
            }
            for t in self.get_lib().get_tour_operator_list()
        ]

    # ---------- менеджеры ----------
    def read_managers(self):
        for m in self.get_data().get('managers', []):
            self.get_lib().create_manager(
                m.get('code', 0),
                m.get('surname', ''),
                m.get('name', ''),
                m.get('secname', ''),
                m.get('position', ''),
                m.get('phone', ''),
                m.get('email', ''),
            )

    def write_managers(self):
        self.get_data()['managers'] = [
            {
                'code': m.get_code(),
                'surname': m.get_surname(),
                'name': m.get_name(),
                'secname': m.get_secname(),
                'position': m.get_position(),
                'phone': m.get_phone(),
                'email': m.get_email(),
            }
            for m in self.get_lib().get_manager_list()
        ]

    # ---------- платежи ----------
    def read_payments(self):
        for p in self.get_data().get('payments', []):
            self.get_lib().create_payment(
                p.get('code', 0),
                p.get('package_code', 0),
                p.get('date', ''),
                p.get('amount', 0),
                p.get('method', ''),
                p.get('status', 'в ожидании'),
            )

    def write_payments(self):
        self.get_data()['payments'] = [
            {
                'code': p.get_code(),
                'package_code': p.get_package_code(),
                'date': p.get_date(),
                'amount': p.get_amount(),
                'method': p.get_method(),
                'status': p.get_status(),
            }
            for p in self.get_lib().get_payment_list()
        ]
