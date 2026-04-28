"""CherryPy-страница для управления путёвками.

Поддерживает все FK расширенной модели: авиаперевозчик, туроператор,
менеджер; а также мульти-связи с клиентами и маршрутами и навигацию
к связанному платежу.
"""

from web.layout import page, esc, back_link, status_badge


class travelpage:

    def __init__(self, library):
        self.__lib = library

    # ---------- список ----------
    def index(self):
        rows = []
        for i, t in enumerate(self.__lib.getTravelList(), 1):
            airline = self.__lib.getAirline(t.getAirlineCode()) if hasattr(t, 'getAirlineCode') else None
            op = self.__lib.getTourOperator(t.getTourOperatorCode()) if hasattr(t, 'getTourOperatorCode') else None
            mgr = self.__lib.getManager(t.getManagerCode()) if hasattr(t, 'getManagerCode') else None
            pay = self.__lib.getPaymentByPackage(t.getCode()) if hasattr(self.__lib, 'getPaymentByPackage') else None
            client_names = []
            for client_code in t.getClientCodes():
                client = self.__lib.getClient(client_code)
                if client is not None:
                    client_names.append(
                        f'{esc(client.getSurname())} {esc(client.getName())}'
                    )
                else:
                    client_names.append(f'<span class="muted">клиент #{client_code}</span>')
            client_count = len(client_names)
            clients_str = ', '.join(client_names) if client_names else '—'

            route_names = []
            for route_code in t.getRouteCodes():
                route = self.__lib.getRoute(route_code)
                if route is not None:
                    route_names.append(esc(route.getName()))
                else:
                    route_names.append(f'<span class="muted">маршрут #{route_code}</span>')
            routes_str = ', '.join(route_names) if route_names else '—'
            airline_str = esc(airline.getName()) if airline else '<span class="muted">—</span>'
            op_str = esc(op.getName()) if op else '<span class="muted">—</span>'
            mgr_str = esc(mgr.getFullName()) if mgr else '<span class="muted">—</span>'
            if pay is not None:
                pay_amount_str = f'{pay.getAmount():,} ₽'
                pay_status_str = status_badge(pay.getStatus())
            else:
                pay_amount_str = '<span class="muted">—</span>'
                pay_status_str = '<span class="muted">—</span>'
            rows.append(
                f'<tr><td>{i}</td><td>{t.getCode()}</td>'
                f'<td>{esc(t.getDate())}</td>'
                f'<td>{client_count or t.getQuantity()}</td>'
                f'<td>{t.getDiscount()}%</td>'
                f'<td>{clients_str}</td><td>{routes_str}</td>'
                f'<td>{airline_str}</td><td>{op_str}</td><td>{mgr_str}</td>'
                f'<td>{pay_amount_str}</td><td>{pay_status_str}</td>'
                f'<td><a href="editform?code={t.getCode()}">изменить</a> · '
                f'<a href="delr?code={t.getCode()}" '
                f'onclick="return confirm(\'Удалить путёвку?\')">удалить</a></td>'
                f'</tr>')
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
            t = self.__lib.getTravel(int(code))
            if t is None:
                raise ValueError('не найдена')
            return page(f'Изменить путёвку №{code}',
                        self._form('editaction', t, int(code)))
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link())
    editform.exposed = True

    def addaction(self, date='', quantity=1, discount=0,
                  airline_code=0, touroperator_code=0, manager_code=0,
                  clients=None, routes=None):
        try:
            clients = self._as_list(clients)
            routes = self._as_list(routes)
            # Количество путёвок синхронизируем с числом выбранных клиентов.
            # Если клиентов пока не выбрали, оставляем введённое вручную значение.
            final_quantity = len(clients) if clients else int(quantity)
            code = self.__lib.getTravelNewCode()
            travel = self.__lib.createTravel(
                code, date.strip(), final_quantity, int(discount),
                int(airline_code or 0), int(touroperator_code or 0),
                int(manager_code or 0))
            for cc in clients:
                travel.appendClient(int(cc))
            for rc in routes:
                travel.appendRoute(int(rc))
            return page('Готово', f'<p>Путёвка №{code} создана.</p>' + back_link())
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link('addform'))
    addaction.exposed = True

    def editaction(self, code=0, date='', quantity=1, discount=0,
                   airline_code=0, touroperator_code=0, manager_code=0,
                   clients=None, routes=None):
        try:
            code = int(code)
            clients = self._as_list(clients)
            routes = self._as_list(routes)
            # Количество путёвок синхронизируем с числом выбранных клиентов.
            # Если клиентов пока не выбрали, оставляем введённое вручную значение.
            final_quantity = len(clients) if clients else int(quantity)
            # сохраняем платёж если был — он привязан к путёвке через FK
            pay = self.__lib.getPaymentByPackage(code)
            saved_pay = None
            if pay is not None:
                saved_pay = (pay.getCode(), pay.getDate(), pay.getAmount(),
                             pay.getMethod(), pay.getStatus())
                self.__lib.removePayment(pay)
            self.__lib.removeTravel(code)
            travel = self.__lib.createTravel(
                code, date.strip(), final_quantity, int(discount),
                int(airline_code or 0), int(touroperator_code or 0),
                int(manager_code or 0))
            for cc in clients:
                travel.appendClient(int(cc))
            for rc in routes:
                travel.appendRoute(int(rc))
            if saved_pay is not None:
                self.__lib.createPayment(saved_pay[0], code, saved_pay[1],
                                         saved_pay[2], saved_pay[3], saved_pay[4])
            return page('Готово', f'<p>Путёвка №{code} обновлена.</p>' + back_link())
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link())
    editaction.exposed = True

    def delr(self, code=0):
        try:
            self.__lib.removeTravel(int(code))
            return page('Готово', f'<p>Путёвка №{code} удалена.</p>' + back_link())
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link())
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
        date = esc(t.getDate()) if t else ''
        qty = t.getQuantity() if t else 1
        disc = t.getDiscount() if t else 0
        ac = t.getAirlineCode() if t and hasattr(t, 'getAirlineCode') else 0
        oc = t.getTourOperatorCode() if t and hasattr(t, 'getTourOperatorCode') else 0
        mc = t.getManagerCode() if t and hasattr(t, 'getManagerCode') else 0
        sel_clients = set(t.getClientCodes()) if t else set()
        sel_routes = set(t.getRouteCodes()) if t else set()

        airline_opts = '<option value="0">— не выбран —</option>'
        for a in self.__lib.getAirlineList():
            sel = ' selected' if a.getCode() == ac else ''
            airline_opts += (f'<option value="{a.getCode()}"{sel}>'
                             f'{esc(a.getName())} ({a.getFlightCost():,} ₽)</option>')

        op_opts = '<option value="0">— не выбран —</option>'
        for o in self.__lib.getTourOperatorList():
            sel = ' selected' if o.getCode() == oc else ''
            op_opts += f'<option value="{o.getCode()}"{sel}>{esc(o.getName())}</option>'

        mgr_opts = '<option value="0">— не выбран —</option>'
        for m in self.__lib.getManagerList():
            sel = ' selected' if m.getCode() == mc else ''
            mgr_opts += (f'<option value="{m.getCode()}"{sel}>'
                         f'{esc(m.getFullName())}</option>')

        client_opts = ''
        for c in self.__lib.getClientList():
            sel = ' selected' if c.getCode() in sel_clients else ''
            client_opts += (f'<option value="{c.getCode()}"{sel}>'
                            f'{esc(c.getSurname())} {esc(c.getName())} '
                            f'(код {c.getCode()})</option>')

        route_opts = ''
        for r in self.__lib.getRouteList():
            sel = ' selected' if r.getCode() in sel_routes else ''
            route_opts += (f'<option value="{r.getCode()}"{sel}>'
                           f'{esc(r.getName())} — {esc(r.getHotel())} '
                           f'({r.getDuration()} дн.)</option>')

        return f'''
<form action="{action}" method="post">
{hidden}
<table>
<tr><td>Дата отправления:</td><td><input name="date" value="{date}" placeholder="ДД.ММ.ГГГГ"></td></tr>
<tr><td>Количество:</td><td><input type="number" name="quantity" value="{qty}" min="1"></td></tr>
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
