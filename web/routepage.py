"""CherryPy-страница для управления маршрутами."""

from web.layout import page, esc, back_link


class routepage:

    def __init__(self, library):
        self.__lib = library

    def index(self):
        rows = []
        for i, r in enumerate(self.__lib.getRouteList(), 1):
            rows.append(
                f'<tr><td>{i}</td><td>{r.getCode()}</td>'
                f'<td>{esc(r.getName())}</td>'
                f'<td>{esc(r.getClimate())}</td>'
                f'<td>{r.getDuration()}</td>'
                f'<td>{esc(r.getHotel())}</td>'
                f'<td>{r.getCost():,} ₽</td>'
                f'<td><a href="editform?code={r.getCode()}">изменить</a> · '
                f'<a href="delr?code={r.getCode()}" '
                f'onclick="return confirm(\'Удалить маршрут?\')">удалить</a></td>'
                f'</tr>')
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
            code = self.__lib.getRouteNewCode()
            self.__lib.createRoute(code, name.strip(), climate.strip(),
                                   int(duration), hotel.strip(), int(cost))
            return page('Готово',
                        f'<p>Маршрут №{code} добавлен.</p>' + back_link())
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link('addform'))
    addaction.exposed = True

    def editform(self, code=0):
        try:
            r = self.__lib.getRoute(int(code))
            if r is None:
                raise ValueError('не найден')
            return page(f'Изменить маршрут №{code}',
                        self._form('editaction', r, int(code)))
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link())
    editform.exposed = True

    def editaction(self, code=0, name='', climate='', duration=0, hotel='', cost=0):
        try:
            code = int(code)
            self.__lib.removeRoute(code)
            self.__lib.createRoute(code, name.strip(), climate.strip(),
                                   int(duration), hotel.strip(), int(cost))
            return page('Готово',
                        f'<p>Маршрут №{code} обновлён.</p>' + back_link())
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link())
    editaction.exposed = True

    def delr(self, code=0):
        try:
            self.__lib.removeRoute(int(code))
            return page('Готово', f'<p>Маршрут №{code} удалён.</p>' + back_link())
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link())
    delr.exposed = True

    def _form(self, action, obj=None, hidden_code=None):
        hidden = (f'<input type="hidden" name="code" value="{hidden_code}">'
                  if hidden_code is not None else '')
        v = lambda fn: esc(fn()) if obj is not None else ''
        return f'''
<form action="{action}" method="post">
{hidden}
<table>
<tr><td>Страна:</td><td><input name="name" value="{v(obj.getName) if obj else ''}"></td></tr>
<tr><td>Климат:</td><td><input name="climate" value="{v(obj.getClimate) if obj else ''}"></td></tr>
<tr><td>Длительность (дней):</td><td><input type="number" name="duration" value="{obj.getDuration() if obj else 7}"></td></tr>
<tr><td>Отель:</td><td><input name="hotel" value="{v(obj.getHotel) if obj else ''}"></td></tr>
<tr><td>Стоимость, ₽:</td><td><input type="number" name="cost" value="{obj.getCost() if obj else 50000}"></td></tr>
<tr><td colspan="2"><input type="submit" value="Сохранить"></td></tr>
</table>
</form>
{back_link()}'''
