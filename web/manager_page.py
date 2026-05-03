"""CherryPy-страница для управления менеджерами."""

from web.layout import (
    page, esc, back_link, field_val, crud_ok, crud_err, crud_row_actions,
)


class ManagerPage:

    def __init__(self, library):
        self.__lib = library

    def index(self):
        rows = []
        for i, m in enumerate(self.__lib.get_manager_list(), 1):
            email = (f'<a href="mailto:{esc(m.get_email())}">{esc(m.get_email())}</a>'
                     if m.get_email() else '<span class="muted">—</span>')
            rows.append(
                f'<tr><td>{i}</td><td>{m.get_code()}</td>'
                f'<td>{esc(m.get_full_name())}</td>'
                f'<td>{esc(m.get_position())}</td>'
                f'<td>{esc(m.get_phone())}</td>'
                f'<td>{email}</td>'
                + crud_row_actions(m.get_code(), 'Удалить менеджера?')
                + '</tr>')
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
            code = self.__lib.get_manager_new_code()
            self.__lib.create_manager(code, surname.strip(), name.strip(),
                                     secname.strip(), position.strip(),
                                     phone.strip(), email.strip())
            return crud_ok(f'<p>Менеджер №{code} добавлен.</p>')
        except Exception as e:
            return crud_err(e, 'addform')
    addaction.exposed = True

    def editform(self, code=0):
        try:
            m = self.__lib.get_manager(int(code))
            if m is None:
                raise ValueError('не найден')
            return page(f'Изменить менеджера №{code}',
                        self._form('editaction', m, int(code)))
        except Exception as e:
            return crud_err(e)
    editform.exposed = True

    def editaction(self, code=0, surname='', name='', secname='',
                   position='', phone='', email=''):
        try:
            code = int(code)
            self.__lib.remove_manager(code)
            self.__lib.create_manager(code, surname.strip(), name.strip(),
                                     secname.strip(), position.strip(),
                                     phone.strip(), email.strip())
            return crud_ok(f'<p>Менеджер №{code} обновлён.</p>')
        except Exception as e:
            return crud_err(e)
    editaction.exposed = True

    def delr(self, code=0):
        try:
            self.__lib.remove_manager(int(code))
            return crud_ok(f'<p>Менеджер №{code} удалён.</p>')
        except Exception as e:
            return crud_err(e)
    delr.exposed = True

    def _form(self, action, obj=None, hidden_code=None):
        hidden = (f'<input type="hidden" name="code" value="{hidden_code}">'
                  if hidden_code is not None else '')
        return f'''
<form action="{action}" method="post">
{hidden}
<table>
<tr><td>Фамилия:</td><td><input name="surname" value="{field_val(obj, 'get_surname')}"></td></tr>
<tr><td>Имя:</td><td><input name="name" value="{field_val(obj, 'get_name')}"></td></tr>
<tr><td>Отчество:</td><td><input name="secname" value="{field_val(obj, 'get_secname')}"></td></tr>
<tr><td>Должность:</td><td><input name="position" value="{field_val(obj, 'get_position')}" size="40"></td></tr>
<tr><td>Телефон:</td><td><input name="phone" value="{field_val(obj, 'get_phone')}"></td></tr>
<tr><td>Email:</td><td><input type="email" name="email" value="{field_val(obj, 'get_email')}" size="40"></td></tr>
<tr><td colspan="2"><input type="submit" value="Сохранить"></td></tr>
</table>
</form>
{back_link()}'''
