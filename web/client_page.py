"""CherryPy-страница для управления клиентами."""

from web.layout import (
    page, esc, back_link, field_val, crud_ok, crud_err, crud_row_actions,
)


class ClientPage:
    """CRUD-страница клиентов."""

    def __init__(self, library):
        self.__lib = library

    @staticmethod
    def _full_name(client):
        """ФИО для таблицы: фамилия, имя, отчество через пробел."""
        parts = [(client.get_surname() or '').strip(),
                 (client.get_name() or '').strip(),
                 (client.get_secname() or '').strip()]
        text = ' '.join(p for p in parts if p)
        return esc(text) if text else '—'

    def index(self):
        rows = []
        for i, c in enumerate(self.__lib.get_client_list(), 1):
            rows.append(
                f'<tr><td>{i}</td><td>{c.get_code()}</td>'
                f'<td>{self._full_name(c)}</td>'
                f'<td>{esc(c.get_address())}</td>'
                f'<td>{esc(c.get_phone())}</td>'
                + crud_row_actions(c.get_code(), 'Удалить клиента?')
                + '</tr>')
        body = (
            '<p><a href="addform">+ Добавить клиента</a></p>'
            '<table><tr><th>№</th><th>Код</th><th>ФИО</th>'
            '<th>Адрес</th><th>Телефон</th><th>Действия</th></tr>'
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
            code = self.__lib.get_client_new_code()
            self.__lib.create_client(code, surname.strip(), name.strip(),
                                    secname.strip(), address.strip(), phone.strip())
            return crud_ok(f'<p>Клиент №{code} добавлен.</p>')
        except Exception as e:
            return crud_err(e, 'addform')
    addaction.exposed = True

    def editform(self, code=0):
        try:
            c = self.__lib.get_client(int(code))
            if c is None:
                raise ValueError('не найден')
            body = self._form('editaction', f'Изменить клиента №{code}',
                              c, hidden_code=int(code))
            return page(f'Редактировать клиента №{code}', body)
        except Exception as e:
            return crud_err(e)
    editform.exposed = True

    def editaction(self, code=0, surname='', name='', secname='', address='', phone=''):
        try:
            code = int(code)
            self.__lib.remove_client(code)
            self.__lib.create_client(code, surname.strip(), name.strip(),
                                    secname.strip(), address.strip(), phone.strip())
            return crud_ok(f'<p>Клиент №{code} обновлён.</p>')
        except Exception as e:
            return crud_err(e)
    editaction.exposed = True

    def delr(self, code=0):
        try:
            self.__lib.remove_client(int(code))
            return crud_ok(f'<p>Клиент №{code} удалён.</p>')
        except Exception as e:
            return crud_err(e)
    delr.exposed = True

    def _form(self, action, title, obj=None, hidden_code=None):
        hidden = (f'<input type="hidden" name="code" value="{hidden_code}">'
                  if hidden_code is not None else '')
        return f'''
<form action="{action}" method="post">
{hidden}
<table>
<tr><td>Фамилия:</td><td><input name="surname" value="{field_val(obj, 'get_surname')}"></td></tr>
<tr><td>Имя:</td><td><input name="name" value="{field_val(obj, 'get_name')}"></td></tr>
<tr><td>Отчество:</td><td><input name="secname" value="{field_val(obj, 'get_secname')}"></td></tr>
<tr><td>Адрес:</td><td><input name="address" size="50" value="{field_val(obj, 'get_address')}"></td></tr>
<tr><td>Телефон:</td><td><input name="phone" value="{field_val(obj, 'get_phone')}"></td></tr>
<tr><td colspan="2"><input type="submit" value="{esc(title)}"></td></tr>
</table>
</form>
{back_link()}'''
