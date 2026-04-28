"""CherryPy-страница для управления авиаперевозчиками."""

from web.layout import page, esc, back_link


class airlinepage:

    def __init__(self, library):
        self.__lib = library

    def index(self):
        rows = []
        for i, a in enumerate(self.__lib.getAirlineList(), 1):
            rows.append(
                f'<tr><td>{i}</td><td>{a.getCode()}</td>'
                f'<td>{esc(a.getName())}</td>'
                f'<td>{a.getFlightCost():,} ₽</td>'
                f'<td><a href="editform?code={a.getCode()}">изменить</a> · '
                f'<a href="delr?code={a.getCode()}" '
                f'onclick="return confirm(\'Удалить авиаперевозчика?\')">удалить</a></td>'
                f'</tr>')
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
            code = self.__lib.getAirlineNewCode()
            self.__lib.createAirline(code, name.strip(), int(flight_cost or 0))
            return page('Готово', f'<p>Авиаперевозчик №{code} добавлен.</p>' + back_link())
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link('addform'))
    addaction.exposed = True

    def editform(self, code=0):
        try:
            a = self.__lib.getAirline(int(code))
            if a is None:
                raise ValueError('не найден')
            return page(f'Изменить авиаперевозчика №{code}',
                        self._form('editaction', a, int(code)))
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link())
    editform.exposed = True

    def editaction(self, code=0, name='', flight_cost=0):
        try:
            code = int(code)
            self.__lib.removeAirline(code)
            self.__lib.createAirline(code, name.strip(), int(flight_cost or 0))
            return page('Готово',
                        f'<p>Авиаперевозчик №{code} обновлён.</p>' + back_link())
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link())
    editaction.exposed = True

    def delr(self, code=0):
        try:
            self.__lib.removeAirline(int(code))
            return page('Готово',
                        f'<p>Авиаперевозчик №{code} удалён.</p>' + back_link())
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link())
    delr.exposed = True

    def _form(self, action, obj=None, hidden_code=None):
        hidden = (f'<input type="hidden" name="code" value="{hidden_code}">'
                  if hidden_code is not None else '')
        name = esc(obj.getName()) if obj else ''
        cost = obj.getFlightCost() if obj else 0
        return f'''
<form action="{action}" method="post">
{hidden}
<table>
<tr><td>Название:</td><td><input name="name" value="{name}" size="40"></td></tr>
<tr><td>Стоимость перелёта, ₽:</td><td><input type="number" name="flight_cost" value="{cost}" min="0"></td></tr>
<tr><td colspan="2"><input type="submit" value="Сохранить"></td></tr>
</table>
</form>
{back_link()}'''
