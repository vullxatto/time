"""CherryPy-страница для управления платежами.

Связь с путёвкой 1:1 через FK package_code: одна путёвка — один платёж.
Поддерживается параметр ?package_code=N в addform для предзаполнения формы
при переходе со страницы путёвок.
"""

from web.layout import page, esc, back_link, status_badge
from domain.payment import PAYMENT_METHODS, PAYMENT_STATUSES


class paymentpage:

    def __init__(self, library):
        self.__lib = library

    def index(self):
        rows = []
        for i, p in enumerate(self.__lib.getPaymentList(), 1):
            travel = self.__lib.getTravel(p.getPackageCode())
            travel_str = (f'№{p.getPackageCode()} от {esc(travel.getDate())}'
                          if travel else f'<span class="muted">№{p.getPackageCode()} (нет)</span>')
            rows.append(
                f'<tr><td>{i}</td><td>{p.getCode()}</td>'
                f'<td>{travel_str}</td>'
                f'<td>{esc(p.getDate())}</td>'
                f'<td>{p.getAmount():,} ₽</td>'
                f'<td>{esc(p.getMethod())}</td>'
                f'<td>{status_badge(p.getStatus())}</td>'
                f'<td><a href="editform?code={p.getCode()}">изменить</a> · '
                f'<a href="delr?code={p.getCode()}" '
                f'onclick="return confirm(\'Удалить платёж?\')">удалить</a></td>'
                f'</tr>')
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
            if self.__lib.getTravel(pkg) is None:
                raise ValueError(f'Путёвка №{pkg} не существует')
            if self.__lib.getPaymentByPackage(pkg) is not None:
                raise ValueError(f'У путёвки №{pkg} уже есть платёж (связь 1:1)')
            code = self.__lib.getPaymentNewCode()
            self.__lib.createPayment(code, pkg, date.strip(), int(amount or 0),
                                     method.strip(), status.strip())
            return page('Готово',
                        f'<p>Платёж №{code} добавлен.</p>' + back_link())
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link('addform'))
    addaction.exposed = True

    def editform(self, code=0):
        try:
            p = self.__lib.getPayment(int(code))
            if p is None:
                raise ValueError('не найден')
            return page(f'Изменить платёж №{code}',
                        self._form('editaction', obj=p, hidden_code=int(code)))
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link())
    editform.exposed = True

    def editaction(self, code=0, package_code=0, date='', amount=0,
                   method='', status='в ожидании'):
        try:
            code = int(code)
            pkg = int(package_code or 0)
            self.__lib.removePayment(code)
            self.__lib.createPayment(code, pkg, date.strip(), int(amount or 0),
                                     method.strip(), status.strip())
            return page('Готово',
                        f'<p>Платёж №{code} обновлён.</p>' + back_link())
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link())
    editaction.exposed = True

    def delr(self, code=0):
        try:
            self.__lib.removePayment(int(code))
            return page('Готово', f'<p>Платёж №{code} удалён.</p>' + back_link())
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link())
    delr.exposed = True

    def _form(self, action, obj=None, hidden_code=None, preset_package=0):
        hidden = (f'<input type="hidden" name="code" value="{hidden_code}">'
                  if hidden_code is not None else '')
        cur_pkg = obj.getPackageCode() if obj else preset_package
        date = esc(obj.getDate()) if obj else ''
        amount = obj.getAmount() if obj else 0
        method = obj.getMethod() if obj else ''
        status = obj.getStatus() if obj else 'в ожидании'

        # выпадающий список путёвок: только те, что без платежа,
        # плюс текущая (при редактировании) для возможности её сохранить
        free_pkgs = []
        for t in self.__lib.getTravelList():
            existing = self.__lib.getPaymentByPackage(t.getCode())
            if existing is None or t.getCode() == cur_pkg:
                free_pkgs.append(t)

        pkg_opts = '<option value="0">— выберите путёвку —</option>'
        for t in free_pkgs:
            sel = ' selected' if t.getCode() == cur_pkg else ''
            client_count = len(t.getClientCodes())
            pkg_opts += (f'<option value="{t.getCode()}"{sel}>'
                         f'№{t.getCode()} от {esc(t.getDate())} '
                         f'({client_count} чел., {t.getQuantity()} шт.)</option>')

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
