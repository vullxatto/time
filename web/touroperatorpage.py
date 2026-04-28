"""CherryPy-страница для управления туроператорами."""

from web.layout import page, esc, back_link


class touroperatorpage:

    def __init__(self, library):
        self.__lib = library

    def index(self):
        rows = []
        for i, t in enumerate(self.__lib.getTourOperatorList(), 1):
            site = (f'<a href="{esc(t.getWebsite())}" target="_blank">{esc(t.getWebsite())}</a>'
                    if t.getWebsite() else '<span class="muted">—</span>')
            rows.append(
                f'<tr><td>{i}</td><td>{t.getCode()}</td>'
                f'<td>{esc(t.getName())}</td>'
                f'<td>{esc(t.getAddress())}</td>'
                f'<td>{esc(t.getPhone())}</td>'
                f'<td>{site}</td>'
                f'<td><a href="editform?code={t.getCode()}">изменить</a> · '
                f'<a href="delr?code={t.getCode()}" '
                f'onclick="return confirm(\'Удалить туроператора?\')">удалить</a></td>'
                f'</tr>')
        body = (
            '<p><a href="addform">+ Добавить туроператора</a></p>'
            '<table><tr><th>№</th><th>Код</th><th>Название</th>'
            '<th>Адрес</th><th>Телефон</th><th>Сайт</th><th>Действия</th></tr>'
            + ''.join(rows) + '</table>'
        )
        return page('Туроператоры', body)
    index.exposed = True

    def addform(self):
        return page('Добавить туроператора', self._form('addaction'))
    addform.exposed = True

    def addaction(self, name='', address='', phone='', website=''):
        try:
            code = self.__lib.getTourOperatorNewCode()
            self.__lib.createTourOperator(code, name.strip(), address.strip(),
                                          phone.strip(), website.strip())
            return page('Готово', f'<p>Туроператор №{code} добавлен.</p>' + back_link())
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link('addform'))
    addaction.exposed = True

    def editform(self, code=0):
        try:
            t = self.__lib.getTourOperator(int(code))
            if t is None:
                raise ValueError('не найден')
            return page(f'Изменить туроператора №{code}',
                        self._form('editaction', t, int(code)))
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link())
    editform.exposed = True

    def editaction(self, code=0, name='', address='', phone='', website=''):
        try:
            code = int(code)
            self.__lib.removeTourOperator(code)
            self.__lib.createTourOperator(code, name.strip(), address.strip(),
                                          phone.strip(), website.strip())
            return page('Готово',
                        f'<p>Туроператор №{code} обновлён.</p>' + back_link())
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link())
    editaction.exposed = True

    def delr(self, code=0):
        try:
            self.__lib.removeTourOperator(int(code))
            return page('Готово',
                        f'<p>Туроператор №{code} удалён.</p>' + back_link())
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
<tr><td>Название:</td><td><input name="name" value="{v(obj.getName) if obj else ''}" size="40"></td></tr>
<tr><td>Адрес:</td><td><input name="address" value="{v(obj.getAddress) if obj else ''}" size="50"></td></tr>
<tr><td>Телефон:</td><td><input name="phone" value="{v(obj.getPhone) if obj else ''}"></td></tr>
<tr><td>Сайт:</td><td><input name="website" value="{v(obj.getWebsite) if obj else ''}" size="40"></td></tr>
<tr><td colspan="2"><input type="submit" value="Сохранить"></td></tr>
</table>
</form>
{back_link()}'''
