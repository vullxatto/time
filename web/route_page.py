"""CherryPy-страница для управления маршрутами."""

from web.layout import (
    page, esc, back_link, field_val, crud_ok, crud_err, crud_row_actions,
)


class RoutePage:

    def __init__(self, library):
        self.__lib = library

    def index(self):
        rows = []
        for i, r in enumerate(self.__lib.get_route_list(), 1):
            rows.append(
                f'<tr><td>{i}</td><td>{r.get_code()}</td>'
                f'<td>{esc(r.get_name())}</td>'
                f'<td>{esc(r.get_climate())}</td>'
                f'<td>{r.get_duration()}</td>'
                f'<td>{esc(r.get_hotel())}</td>'
                f'<td>{r.get_cost():,} ₽</td>'
                + crud_row_actions(r.get_code(), 'Удалить маршрут?')
                + '</tr>')
        body = (
            '<p><a href="addform">+ Добавить маршрут</a></p>'
            '<table><tr><th>№</th><th>Код</th><th>Страна</th><th>Климат</th>'
            '<th>Дней</th><th>Отель</th><th>Стоимость</th><th>Действия</th></tr>'
            + ''.join(rows) + '</table>'
        )
        return page('Маршруты', body)
    index.exposed = True

    def addform(self):
        return page('Добавить маршрут', self._form('addaction'))
    addform.exposed = True

    def addaction(self, name='', climate='', duration=0, hotel='', cost=0):
        try:
            code = self.__lib.get_route_new_code()
            self.__lib.create_route(code, name.strip(), climate.strip(),
                                   int(duration), hotel.strip(), int(cost))
            return crud_ok(f'<p>Маршрут №{code} добавлен.</p>')
        except Exception as e:
            return crud_err(e, 'addform')
    addaction.exposed = True

    def editform(self, code=0):
        try:
            r = self.__lib.get_route(int(code))
            if r is None:
                raise ValueError('не найден')
            return page(f'Изменить маршрут №{code}',
                        self._form('editaction', r, int(code)))
        except Exception as e:
            return crud_err(e)
    editform.exposed = True

    def editaction(self, code=0, name='', climate='', duration=0, hotel='', cost=0):
        try:
            code = int(code)
            self.__lib.remove_route(code)
            self.__lib.create_route(code, name.strip(), climate.strip(),
                                   int(duration), hotel.strip(), int(cost))
            return crud_ok(f'<p>Маршрут №{code} обновлён.</p>')
        except Exception as e:
            return crud_err(e)
    editaction.exposed = True

    def delr(self, code=0):
        try:
            self.__lib.remove_route(int(code))
            return crud_ok(f'<p>Маршрут №{code} удалён.</p>')
        except Exception as e:
            return crud_err(e)
    delr.exposed = True

    def _form(self, action, obj=None, hidden_code=None):
        hidden = (f'<input type="hidden" name="code" value="{hidden_code}">'
                  if hidden_code is not None else '')
        dur = obj.get_duration() if obj else 7
        cost = obj.get_cost() if obj else 50000
        return f'''
<form action="{action}" method="post">
{hidden}
<table>
<tr><td>Страна:</td><td><input name="name" value="{field_val(obj, 'get_name')}"></td></tr>
<tr><td>Климат:</td><td><input name="climate" value="{field_val(obj, 'get_climate')}"></td></tr>
<tr><td>Длительность (дней):</td><td><input type="number" name="duration" value="{dur}"></td></tr>
<tr><td>Отель:</td><td><input name="hotel" value="{field_val(obj, 'get_hotel')}"></td></tr>
<tr><td>Стоимость, ₽:</td><td><input type="number" name="cost" value="{cost}"></td></tr>
<tr><td colspan="2"><input type="submit" value="Сохранить"></td></tr>
</table>
</form>
{back_link()}'''
