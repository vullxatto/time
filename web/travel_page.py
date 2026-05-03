"""CherryPy-страница для управления путёвками.

Поддерживает все FK расширенной модели: авиаперевозчик, туроператор,
менеджер; а также мульти-связи с клиентами и маршрутами и навигацию
к связанному платежу.
"""

from web.layout import (
    page, esc, back_link, status_badge, crud_ok, crud_err, crud_row_actions,
)


class TravelPage:

    def __init__(self, library):
        self.__lib = library

    @staticmethod
    def _client_fio(client):
        """Фамилия, имя, отчество одной строкой (уже с esc)."""
        parts = [(client.get_surname() or '').strip(),
                 (client.get_name() or '').strip(),
                 (client.get_secname() or '').strip()]
        text = ' '.join(p for p in parts if p)
        return esc(text) if text else ''

    # ---------- список ----------
    def index(self):
        rows = []
        for i, t in enumerate(self.__lib.get_travel_list(), 1):
            airline = self.__lib.get_airline(t.get_airline_code()) if hasattr(t, 'get_airline_code') else None
            op = self.__lib.get_tour_operator(t.get_tour_operator_code()) if hasattr(t, 'get_tour_operator_code') else None
            mgr = self.__lib.get_manager(t.get_manager_code()) if hasattr(t, 'get_manager_code') else None
            pay = self.__lib.get_payment_by_package(t.get_code()) if hasattr(self.__lib, 'get_payment_by_package') else None
            client_names = []
            for client_code in t.get_client_codes():
                client = self.__lib.get_client(client_code)
                if client is not None:
                    label = TravelPage._client_fio(client)
                    client_names.append(label if label else '—')
                else:
                    client_names.append(f'<span class="muted">клиент #{client_code}</span>')
            client_count = len(client_names)
            clients_str = ', '.join(client_names) if client_names else '—'

            route_names = []
            for route_code in t.get_route_codes():
                route = self.__lib.get_route(route_code)
                if route is not None:
                    route_names.append(esc(route.get_name()))
                else:
                    route_names.append(f'<span class="muted">маршрут #{route_code}</span>')
            routes_str = ', '.join(route_names) if route_names else '—'
            airline_str = esc(airline.get_name()) if airline else '<span class="muted">—</span>'
            op_str = esc(op.get_name()) if op else '<span class="muted">—</span>'
            mgr_str = esc(mgr.get_full_name()) if mgr else '<span class="muted">—</span>'
            if pay is not None:
                pay_amount_str = f'{pay.get_amount():,} ₽'
                pay_status_str = status_badge(pay.get_status())
            else:
                pay_amount_str = '<span class="muted">—</span>'
                pay_status_str = '<span class="muted">—</span>'
            qty_cell = (
                str(client_count)
                if client_count else '<span class="muted">—</span>')
            rows.append(
                f'<tr><td>{i}</td><td>{t.get_code()}</td>'
                f'<td>{esc(t.get_date())}</td>'
                f'<td>{qty_cell}</td>'
                f'<td>{t.get_discount()}%</td>'
                f'<td>{clients_str}</td><td>{routes_str}</td>'
                f'<td>{airline_str}</td><td>{op_str}</td><td>{mgr_str}</td>'
                f'<td>{pay_amount_str}</td><td>{pay_status_str}</td>'
                + crud_row_actions(t.get_code(), 'Удалить путёвку?')
                + '</tr>')
        body = (
            '<p><a href="addform">+ Добавить путёвку</a></p>'
            '<table><tr><th>№</th><th>Код</th><th>Дата</th><th>Кол-во</th>'
            '<th>Скидка</th><th>Клиенты</th><th>Маршруты</th>'
            '<th>Авиа</th><th>Туроператор</th><th>Менеджер</th>'
            '<th>Сумма</th><th>Статус</th><th>Действия</th></tr>'
            + ''.join(rows) + '</table>'
        )
        return page('Путёвки', body)
    index.exposed = True

    # ---------- формы ----------
    def addform(self):
        return page('Добавить путёвку', self._form('addaction'))
    addform.exposed = True

    def editform(self, code=0):
        try:
            t = self.__lib.get_travel(int(code))
            if t is None:
                raise ValueError('не найдена')
            return page(f'Изменить путёвку №{code}',
                        self._form('editaction', t, int(code)))
        except Exception as e:
            return crud_err(e)
    editform.exposed = True

    def addaction(self, date='', discount=0,
                  airline_code=0, touroperator_code=0, manager_code=0,
                  clients=None, routes=None):
        try:
            clients = self._as_list(clients)
            routes = self._as_list(routes)
            final_quantity = len(clients)
            code = self.__lib.get_travel_new_code()
            travel = self.__lib.create_travel(
                code, date.strip(), final_quantity, int(discount),
                int(airline_code or 0), int(touroperator_code or 0),
                int(manager_code or 0))
            for cc in clients:
                travel.append_client(int(cc))
            for rc in routes:
                travel.append_route(int(rc))
            return crud_ok(f'<p>Путёвка №{code} создана.</p>')
        except Exception as e:
            return crud_err(e, 'addform')
    addaction.exposed = True

    def editaction(self, code=0, date='', discount=0,
                   airline_code=0, touroperator_code=0, manager_code=0,
                   clients=None, routes=None):
        try:
            code = int(code)
            clients = self._as_list(clients)
            routes = self._as_list(routes)
            final_quantity = len(clients)
            # сохраняем платёж если был — он привязан к путёвке через FK
            pay = self.__lib.get_payment_by_package(code)
            saved_pay = None
            if pay is not None:
                saved_pay = (pay.get_code(), pay.get_date(), pay.get_amount(),
                             pay.get_method(), pay.get_status())
                self.__lib.remove_payment(pay)
            self.__lib.remove_travel(code)
            travel = self.__lib.create_travel(
                code, date.strip(), final_quantity, int(discount),
                int(airline_code or 0), int(touroperator_code or 0),
                int(manager_code or 0))
            for cc in clients:
                travel.append_client(int(cc))
            for rc in routes:
                travel.append_route(int(rc))
            if saved_pay is not None:
                self.__lib.create_payment(saved_pay[0], code, saved_pay[1],
                                         saved_pay[2], saved_pay[3], saved_pay[4])
            return crud_ok(f'<p>Путёвка №{code} обновлена.</p>')
        except Exception as e:
            return crud_err(e)
    editaction.exposed = True

    def delr(self, code=0):
        try:
            self.__lib.remove_travel(int(code))
            return crud_ok(f'<p>Путёвка №{code} удалена.</p>')
        except Exception as e:
            return crud_err(e)
    delr.exposed = True

    # ---------- helpers ----------
    @staticmethod
    def _as_list(value):
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        return list(value)

    def _form(self, action, t=None, hidden_code=None):
        hidden = (f'<input type="hidden" name="code" value="{hidden_code}">'
                  if hidden_code is not None else '')
        date = esc(t.get_date()) if t else ''
        disc = t.get_discount() if t else 0
        ac = t.get_airline_code() if t and hasattr(t, 'get_airline_code') else 0
        oc = t.get_tour_operator_code() if t and hasattr(t, 'get_tour_operator_code') else 0
        mc = t.get_manager_code() if t and hasattr(t, 'get_manager_code') else 0
        sel_clients = set(t.get_client_codes()) if t else set()
        sel_routes = set(t.get_route_codes()) if t else set()

        airline_opts = '<option value="0">— не выбран —</option>'
        for a in self.__lib.get_airline_list():
            sel = ' selected' if a.get_code() == ac else ''
            airline_opts += (f'<option value="{a.get_code()}"{sel}>'
                             f'{esc(a.get_name())} ({a.get_flight_cost():,} ₽)</option>')

        op_opts = '<option value="0">— не выбран —</option>'
        for o in self.__lib.get_tour_operator_list():
            sel = ' selected' if o.get_code() == oc else ''
            op_opts += f'<option value="{o.get_code()}"{sel}>{esc(o.get_name())}</option>'

        mgr_opts = '<option value="0">— не выбран —</option>'
        for m in self.__lib.get_manager_list():
            sel = ' selected' if m.get_code() == mc else ''
            mgr_opts += (f'<option value="{m.get_code()}"{sel}>'
                         f'{esc(m.get_full_name())}</option>')

        client_opts = ''
        for c in self.__lib.get_client_list():
            sel = ' selected' if c.get_code() in sel_clients else ''
            fio = TravelPage._client_fio(c) or '—'
            client_opts += (f'<option value="{c.get_code()}"{sel}>'
                            f'{fio} (код {c.get_code()})</option>')

        route_opts = ''
        for r in self.__lib.get_route_list():
            sel = ' selected' if r.get_code() in sel_routes else ''
            route_opts += (f'<option value="{r.get_code()}"{sel}>'
                           f'{esc(r.get_name())} — {esc(r.get_hotel())} '
                           f'({r.get_duration()} дн.)</option>')

        return f'''
<form action="{action}" method="post">
{hidden}
<table>
<tr><td>Дата отправления:</td><td><input name="date" value="{date}" placeholder="ДД.ММ.ГГГГ"></td></tr>
<tr><td>Скидка, %:</td><td><input type="number" name="discount" value="{disc}" min="0" max="100"></td></tr>
<tr><td>Авиаперевозчик:</td><td><select name="airline_code">{airline_opts}</select></td></tr>
<tr><td>Туроператор:</td><td><select name="touroperator_code">{op_opts}</select></td></tr>
<tr><td>Менеджер:</td><td><select name="manager_code">{mgr_opts}</select></td></tr>
</table>

<h3>Клиенты <span class="muted">(удерживайте Ctrl для множественного выбора)</span></h3>
<select name="clients" multiple size="6" style="min-width:450px">{client_opts}</select>

<h3>Маршруты <span class="muted">(удерживайте Ctrl)</span></h3>
<select name="routes" multiple size="6" style="min-width:450px">{route_opts}</select>

<p><input type="submit" value="Сохранить"></p>
</form>
{back_link()}'''
