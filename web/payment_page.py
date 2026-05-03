"""CherryPy-страница для управления платежами.

Связь с путёвкой 1:1 через FK package_code: одна путёвка — один платёж.
Поддерживается параметр ?package_code=N в addform для предзаполнения формы
при переходе со страницы путёвок.
"""

from web.layout import (
    page, esc, back_link, status_badge, crud_ok, crud_err, crud_row_actions,
)
from domain.payment import PAYMENT_METHODS, PAYMENT_STATUSES


class PaymentPage:

    def __init__(self, library):
        self.__lib = library

    def index(self):
        rows = []
        for i, p in enumerate(self.__lib.get_payment_list(), 1):
            travel = self.__lib.get_travel(p.get_package_code())
            travel_str = (f'№{p.get_package_code()} от {esc(travel.get_date())}'
                          if travel else f'<span class="muted">№{p.get_package_code()} (нет)</span>')
            rows.append(
                f'<tr><td>{i}</td><td>{p.get_code()}</td>'
                f'<td>{travel_str}</td>'
                f'<td>{esc(p.get_date())}</td>'
                f'<td>{p.get_amount():,} ₽</td>'
                f'<td>{esc(p.get_method())}</td>'
                f'<td>{status_badge(p.get_status())}</td>'
                + crud_row_actions(p.get_code(), 'Удалить платёж?')
                + '</tr>')
        body = (
            '<p><a href="addform">+ Добавить платёж</a></p>'
            '<table><tr><th>№</th><th>Код</th><th>Путёвка</th>'
            '<th>Дата</th><th>Сумма</th><th>Способ</th>'
            '<th>Статус</th><th>Действия</th></tr>'
            + ''.join(rows) + '</table>'
        )
        return page('Платежи', body)
    index.exposed = True

    def addform(self, package_code=0):
        return page('Добавить платёж',
                    self._form('addaction', preset_package=int(package_code or 0)))
    addform.exposed = True

    def addaction(self, package_code=0, date='', amount=0,
                  method='', status='в ожидании'):
        try:
            pkg = int(package_code or 0)
            if pkg <= 0:
                raise ValueError('Не указана путёвка')
            if self.__lib.get_travel(pkg) is None:
                raise ValueError(f'Путёвка №{pkg} не существует')
            if self.__lib.get_payment_by_package(pkg) is not None:
                raise ValueError(f'У путёвки №{pkg} уже есть платёж (связь 1:1)')
            code = self.__lib.get_payment_new_code()
            self.__lib.create_payment(code, pkg, date.strip(), int(amount or 0),
                                     method.strip(), status.strip())
            return crud_ok(f'<p>Платёж №{code} добавлен.</p>')
        except Exception as e:
            return crud_err(e, 'addform')
    addaction.exposed = True

    def editform(self, code=0):
        try:
            p = self.__lib.get_payment(int(code))
            if p is None:
                raise ValueError('не найден')
            return page(f'Изменить платёж №{code}',
                        self._form('editaction', obj=p, hidden_code=int(code)))
        except Exception as e:
            return crud_err(e)
    editform.exposed = True

    def editaction(self, code=0, package_code=0, date='', amount=0,
                   method='', status='в ожидании'):
        try:
            code = int(code)
            pkg = int(package_code or 0)
            self.__lib.remove_payment(code)
            self.__lib.create_payment(code, pkg, date.strip(), int(amount or 0),
                                     method.strip(), status.strip())
            return crud_ok(f'<p>Платёж №{code} обновлён.</p>')
        except Exception as e:
            return crud_err(e)
    editaction.exposed = True

    def delr(self, code=0):
        try:
            self.__lib.remove_payment(int(code))
            return crud_ok(f'<p>Платёж №{code} удалён.</p>')
        except Exception as e:
            return crud_err(e)
    delr.exposed = True

    def _form(self, action, obj=None, hidden_code=None, preset_package=0):
        hidden = (f'<input type="hidden" name="code" value="{hidden_code}">'
                  if hidden_code is not None else '')
        cur_pkg = obj.get_package_code() if obj else preset_package
        date = esc(obj.get_date()) if obj else ''
        amount = obj.get_amount() if obj else 0
        method = obj.get_method() if obj else ''
        status = obj.get_status() if obj else 'в ожидании'

        # выпадающий список путёвок: только те, что без платежа,
        # плюс текущая (при редактировании) для возможности её сохранить
        free_pkgs = []
        for t in self.__lib.get_travel_list():
            existing = self.__lib.get_payment_by_package(t.get_code())
            if existing is None or t.get_code() == cur_pkg:
                free_pkgs.append(t)

        pkg_opts = '<option value="0">— выберите путёвку —</option>'
        for t in free_pkgs:
            sel = ' selected' if t.get_code() == cur_pkg else ''
            client_count = len(t.get_client_codes())
            qty_hint = f'{client_count} чел.' if client_count else 'нет клиентов'
            pkg_opts += (f'<option value="{t.get_code()}"{sel}>'
                         f'№{t.get_code()} от {esc(t.get_date())} '
                         f'({qty_hint})</option>')

        method_opts = ''.join(
            f'<option value="{esc(m)}"{ " selected" if m == method else "" }>{esc(m)}</option>'
            for m in PAYMENT_METHODS
        )
        status_opts = ''.join(
            f'<option value="{esc(s)}"{ " selected" if s == status else "" }>{esc(s)}</option>'
            for s in PAYMENT_STATUSES
        )

        return f'''
<form action="{action}" method="post">
{hidden}
<table>
<tr><td>Путёвка:</td><td><select name="package_code">{pkg_opts}</select></td></tr>
<tr><td>Дата:</td><td><input name="date" value="{date}" placeholder="ДД.ММ.ГГГГ"></td></tr>
<tr><td>Сумма, ₽:</td><td><input type="number" name="amount" value="{amount}" min="0"></td></tr>
<tr><td>Способ:</td><td><select name="method">{method_opts}</select></td></tr>
<tr><td>Статус:</td><td><select name="status">{status_opts}</select></td></tr>
<tr><td colspan="2"><input type="submit" value="Сохранить"></td></tr>
</table>
</form>
{back_link()}'''
