"""CherryPy-страница для управления менеджерами."""

from web.layout import page, esc, back_link


class managerpage:

    def __init__(self, library):
        self.__lib = library

    def index(self):
        rows = []
        for i, m in enumerate(self.__lib.getManagerList(), 1):
            email = (f'<a href="mailto:{esc(m.getEmail())}">{esc(m.getEmail())}</a>'
                     if m.getEmail() else '<span class="muted">—</span>')
            rows.append(
                f'<tr><td>{i}</td><td>{m.getCode()}</td>'
                f'<td>{esc(m.getFullName())}</td>'
                f'<td>{esc(m.getPosition())}</td>'
                f'<td>{esc(m.getPhone())}</td>'
                f'<td>{email}</td>'
                f'<td><a href="editform?code={m.getCode()}">изменить</a> · '
                f'<a href="delr?code={m.getCode()}" '
                f'onclick="return confirm(\'Удалить менеджера?\')">удалить</a></td>'
                f'</tr>')
        body = (
            '<p><a href="addform">+ Добавить менеджера</a></p>'
            '<table><tr><th>№</th><th>Код</th><th>ФИО</th>'
            '<th>Должность</th><th>Телефон</th><th>Email</th><th>Действия</th></tr>'
            + ''.join(rows) + '</table>'
        )
        return page('Менеджеры', body)
    index.exposed = True

    def addform(self):
        return page('Добавить менеджера', self._form('addaction'))
    addform.exposed = True

    def addaction(self, surname='', name='', secname='',
                  position='', phone='', email=''):
        try:
            code = self.__lib.getManagerNewCode()
            self.__lib.createManager(code, surname.strip(), name.strip(),
                                     secname.strip(), position.strip(),
                                     phone.strip(), email.strip())
            return page('Готово',
                        f'<p>Менеджер №{code} добавлен.</p>' + back_link())
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link('addform'))
    addaction.exposed = True

    def editform(self, code=0):
        try:
            m = self.__lib.getManager(int(code))
            if m is None:
                raise ValueError('не найден')
            return page(f'Изменить менеджера №{code}',
                        self._form('editaction', m, int(code)))
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link())
    editform.exposed = True

    def editaction(self, code=0, surname='', name='', secname='',
                   position='', phone='', email=''):
        try:
            code = int(code)
            self.__lib.removeManager(code)
            self.__lib.createManager(code, surname.strip(), name.strip(),
                                     secname.strip(), position.strip(),
                                     phone.strip(), email.strip())
            return page('Готово',
                        f'<p>Менеджер №{code} обновлён.</p>' + back_link())
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link())
    editaction.exposed = True

    def delr(self, code=0):
        try:
            self.__lib.removeManager(int(code))
            return page('Готово',
                        f'<p>Менеджер №{code} удалён.</p>' + back_link())
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
<tr><td>Фамилия:</td><td><input name="surname" value="{v(obj.getSurname) if obj else ''}"></td></tr>
<tr><td>Имя:</td><td><input name="name" value="{v(obj.getName) if obj else ''}"></td></tr>
<tr><td>Отчество:</td><td><input name="secname" value="{v(obj.getSecname) if obj else ''}"></td></tr>
<tr><td>Должность:</td><td><input name="position" value="{v(obj.getPosition) if obj else ''}" size="40"></td></tr>
<tr><td>Телефон:</td><td><input name="phone" value="{v(obj.getPhone) if obj else ''}"></td></tr>
<tr><td>Email:</td><td><input type="email" name="email" value="{v(obj.getEmail) if obj else ''}" size="40"></td></tr>
<tr><td colspan="2"><input type="submit" value="Сохранить"></td></tr>
</table>
</form>
{back_link()}'''
