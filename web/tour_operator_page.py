"""CherryPy-страница для управления туроператорами."""

from web.layout import (
    page, esc, back_link, field_val, crud_ok, crud_err, crud_row_actions,
)


class TourOperatorPage:

    def __init__(self, library):
        self.__lib = library

    def index(self):
        rows = []
        for i, t in enumerate(self.__lib.get_tour_operator_list(), 1):
            site = (f'<a href="{esc(t.get_website())}" target="_blank">{esc(t.get_website())}</a>'
                    if t.get_website() else '<span class="muted">—</span>')
            rows.append(
                f'<tr><td>{i}</td><td>{t.get_code()}</td>'
                f'<td>{esc(t.get_name())}</td>'
                f'<td>{esc(t.get_address())}</td>'
                f'<td>{esc(t.get_phone())}</td>'
                f'<td>{site}</td>'
                + crud_row_actions(t.get_code(), 'Удалить туроператора?')
                + '</tr>')
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
            code = self.__lib.get_tour_operator_new_code()
            self.__lib.create_tour_operator(code, name.strip(), address.strip(),
                                          phone.strip(), website.strip())
            return crud_ok(f'<p>Туроператор №{code} добавлен.</p>')
        except Exception as e:
            return crud_err(e, 'addform')
    addaction.exposed = True

    def editform(self, code=0):
        try:
            t = self.__lib.get_tour_operator(int(code))
            if t is None:
                raise ValueError('не найден')
            return page(f'Изменить туроператора №{code}',
                        self._form('editaction', t, int(code)))
        except Exception as e:
            return crud_err(e)
    editform.exposed = True

    def editaction(self, code=0, name='', address='', phone='', website=''):
        try:
            code = int(code)
            self.__lib.remove_tour_operator(code)
            self.__lib.create_tour_operator(code, name.strip(), address.strip(),
                                          phone.strip(), website.strip())
            return crud_ok(f'<p>Туроператор №{code} обновлён.</p>')
        except Exception as e:
            return crud_err(e)
    editaction.exposed = True

    def delr(self, code=0):
        try:
            self.__lib.remove_tour_operator(int(code))
            return crud_ok(f'<p>Туроператор №{code} удалён.</p>')
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
<tr><td>Название:</td><td><input name="name" value="{field_val(obj, 'get_name')}" size="40"></td></tr>
<tr><td>Адрес:</td><td><input name="address" value="{field_val(obj, 'get_address')}" size="50"></td></tr>
<tr><td>Телефон:</td><td><input name="phone" value="{field_val(obj, 'get_phone')}"></td></tr>
<tr><td>Сайт:</td><td><input name="website" value="{field_val(obj, 'get_website')}" size="40"></td></tr>
<tr><td colspan="2"><input type="submit" value="Сохранить"></td></tr>
</table>
</form>
{back_link()}'''
