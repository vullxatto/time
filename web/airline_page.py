"""CherryPy-страница для управления авиаперевозчиками."""

from web.layout import (
    page, esc, back_link, field_val, crud_ok, crud_err, crud_row_actions,
)


class AirlinePage:

    def __init__(self, library):
        self.__lib = library

    def index(self):
        rows = []
        for i, a in enumerate(self.__lib.get_airline_list(), 1):
            rows.append(
                f'<tr><td>{i}</td><td>{a.get_code()}</td>'
                f'<td>{esc(a.get_name())}</td>'
                f'<td>{a.get_flight_cost():,} ₽</td>'
                + crud_row_actions(a.get_code(), 'Удалить авиаперевозчика?')
                + '</tr>')
        body = (
            '<p><a href="addform">+ Добавить авиаперевозчика</a></p>'
            '<table><tr><th>№</th><th>Код</th><th>Название</th>'
            '<th>Стоимость перелёта</th><th>Действия</th></tr>'
            + ''.join(rows) + '</table>'
        )
        return page('Авиаперевозчики', body)
    index.exposed = True

    def addform(self):
        return page('Добавить авиаперевозчика', self._form('addaction'))
    addform.exposed = True

    def addaction(self, name='', flight_cost=0):
        try:
            code = self.__lib.get_airline_new_code()
            self.__lib.create_airline(code, name.strip(), int(flight_cost or 0))
            return crud_ok(f'<p>Авиаперевозчик №{code} добавлен.</p>')
        except Exception as e:
            return crud_err(e, 'addform')
    addaction.exposed = True

    def editform(self, code=0):
        try:
            a = self.__lib.get_airline(int(code))
            if a is None:
                raise ValueError('не найден')
            return page(f'Изменить авиаперевозчика №{code}',
                        self._form('editaction', a, int(code)))
        except Exception as e:
            return crud_err(e)
    editform.exposed = True

    def editaction(self, code=0, name='', flight_cost=0):
        try:
            code = int(code)
            self.__lib.remove_airline(code)
            self.__lib.create_airline(code, name.strip(), int(flight_cost or 0))
            return crud_ok(f'<p>Авиаперевозчик №{code} обновлён.</p>')
        except Exception as e:
            return crud_err(e)
    editaction.exposed = True

    def delr(self, code=0):
        try:
            self.__lib.remove_airline(int(code))
            return crud_ok(f'<p>Авиаперевозчик №{code} удалён.</p>')
        except Exception as e:
            return crud_err(e)
    delr.exposed = True

    def _form(self, action, obj=None, hidden_code=None):
        hidden = (f'<input type="hidden" name="code" value="{hidden_code}">'
                  if hidden_code is not None else '')
        cost = obj.get_flight_cost() if obj else 0
        return f'''
<form action="{action}" method="post">
{hidden}
<table>
<tr><td>Название:</td><td><input name="name" value="{field_val(obj, 'get_name')}" size="40"></td></tr>
<tr><td>Стоимость перелёта, ₽:</td><td><input type="number" name="flight_cost" value="{cost}" min="0"></td></tr>
<tr><td colspan="2"><input type="submit" value="Сохранить"></td></tr>
</table>
</form>
{back_link()}'''
