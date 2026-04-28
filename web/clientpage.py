"""CherryPy-страница для управления клиентами."""

from web.layout import page, esc, back_link


class clientpage:
    """CRUD-страница клиентов."""

    def __init__(self, library):
        self.__lib = library

    def index(self):
        rows = []
        for i, c in enumerate(self.__lib.getClientList(), 1):
            rows.append(
                f'<tr><td>{i}</td><td>{c.getCode()}</td>'
                f'<td>{esc(c.getSurname())}</td>'
                f'<td>{esc(c.getName())}</td>'
                f'<td>{esc(c.getSecname())}</td>'
                f'<td>{esc(c.getAddress())}</td>'
                f'<td>{esc(c.getPhone())}</td>'
                f'<td><a href="editform?code={c.getCode()}">изменить</a> · '
                f'<a href="delr?code={c.getCode()}" '
                f'onclick="return confirm(\'Удалить клиента?\')">удалить</a></td>'
                f'</tr>')
        body = (
            '<p><a href="addform">+ Добавить клиента</a></p>'
            '<table><tr><th>№</th><th>Код</th><th>Фамилия</th><th>Имя</th>'
            '<th>Отчество</th><th>Адрес</th><th>Телефон</th><th>Действия</th></tr>'
            + ''.join(rows) + '</table>'
        )
        return page('Клиенты', body)
    index.exposed = True

    def addform(self):
        body = self._form('addaction', 'Добавить клиента')
        return page('Добавить клиента', body)
    addform.exposed = True

    def addaction(self, surname='', name='', secname='', address='', phone=''):
        try:
            code = self.__lib.getClientNewCode()
            self.__lib.createClient(code, surname.strip(), name.strip(),
                                    secname.strip(), address.strip(), phone.strip())
            return page('Готово',
                        f'<p>Клиент №{code} добавлен.</p>' + back_link())
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link('addform'))
    addaction.exposed = True

    def editform(self, code=0):
        try:
            c = self.__lib.getClient(int(code))
            if c is None:
                raise ValueError('не найден')
            body = self._form('editaction', f'Изменить клиента №{code}',
                              c, hidden_code=int(code))
            return page(f'Редактировать клиента №{code}', body)
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link())
    editform.exposed = True

    def editaction(self, code=0, surname='', name='', secname='', address='', phone=''):
        try:
            code = int(code)
            self.__lib.removeClient(code)
            self.__lib.createClient(code, surname.strip(), name.strip(),
                                    secname.strip(), address.strip(), phone.strip())
            return page('Готово', f'<p>Клиент №{code} обновлён.</p>' + back_link())
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link())
    editaction.exposed = True

    def delr(self, code=0):
        try:
            self.__lib.removeClient(int(code))
            return page('Готово', f'<p>Клиент №{code} удалён.</p>' + back_link())
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link())
    delr.exposed = True

    def _form(self, action, title, obj=None, hidden_code=None):
        v = lambda fn: esc(fn()) if obj is not None else ''
        hidden = (f'<input type="hidden" name="code" value="{hidden_code}">'
                  if hidden_code is not None else '')
        return f'''
<form action="{action}" method="post">
{hidden}
<table>
<tr><td>Фамилия:</td><td><input name="surname" value="{v(obj.getSurname) if obj else ''}"></td></tr>
<tr><td>Имя:</td><td><input name="name" value="{v(obj.getName) if obj else ''}"></td></tr>
<tr><td>Отчество:</td><td><input name="secname" value="{v(obj.getSecname) if obj else ''}"></td></tr>
<tr><td>Адрес:</td><td><input name="address" size="50" value="{v(obj.getAddress) if obj else ''}"></td></tr>
<tr><td>Телефон:</td><td><input name="phone" value="{v(obj.getPhone) if obj else ''}"></td></tr>
<tr><td colspan="2"><input type="submit" value="{esc(title)}"></td></tr>
</table>
</form>
{back_link()}'''
