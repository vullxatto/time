"""Точка входа веб-приложения на CherryPy.

Использует расширенную модель TravelCompanyExt (7 сущностей) и
расширенные сериализаторы JSON/XML/SQL.
"""

import os
import sys
import cherrypy

root_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(root_dir)
sys.path.insert(0, root_dir)

from domain.travel_company_ext import TravelCompanyExt
from dataaccess.data_json_ext import DataJsonExt
from dataaccess.data_xml_ext import DataXmlExt
from dataaccess.data_sql_ext import DataSqlExt
from web.layout import page, esc, back_link
from web.client_page import ClientPage
from web.route_page import RoutePage
from web.travel_page import TravelPage
from web.airline_page import AirlinePage
from web.tour_operator_page import TourOperatorPage
from web.manager_page import ManagerPage
from web.payment_page import PaymentPage


def _detect_format(fname, dformat):
    """Определяет формат файла по расширению; падает обратно на dformat."""
    if isinstance(dformat, (list, tuple)):
        dformat = dformat[0] if dformat else ''
    dformat = (dformat or '').strip()
    ext = os.path.splitext(fname)[1].lower()
    if ext == '.json':
        return 'JSON'
    if ext == '.xml':
        return 'XML'
    if ext in ('.sqlite', '.db'):
        return 'SQL'
    return dformat


class Root:
    """Корневая страница: открытие/сохранение файлов и переход к редакторам."""

    def __init__(self):
        self.__lib = TravelCompanyExt()
        self.__loaded = False
        self.__fname = ''
        self.__fmt = ''
        # сериализаторы переиспользуем
        self.__djson = DataJsonExt(self.__lib)
        self.__dxml = DataXmlExt(self.__lib)
        self.__dsql = DataSqlExt(self.__lib)
        # дочерние страницы (имена атрибутов = URL CherryPy: /clientpage/, …)
        self.clientpage = ClientPage(self.__lib)
        self.routepage = RoutePage(self.__lib)
        self.travelpage = TravelPage(self.__lib)
        self.airlinepage = AirlinePage(self.__lib)
        self.touroperatorpage = TourOperatorPage(self.__lib)
        self.managerpage = ManagerPage(self.__lib)
        self.paymentpage = PaymentPage(self.__lib)

    def index(self):
        if not self.__loaded:
            body = self._open_form('data/demo.json', 'JSON', loaded=False)
            return page('Открыть файл данных', body)
        # сводка
        l = self.__lib
        summary = (
            f'<table>'
            f'<tr><th>Сущность</th><th>Записей</th></tr>'
            f'<tr><td><a href="/clientpage/">Клиенты</a></td><td>{len(l.get_client_list())}</td></tr>'
            f'<tr><td><a href="/routepage/">Маршруты</a></td><td>{len(l.get_route_list())}</td></tr>'
            f'<tr><td><a href="/travelpage/">Путёвки</a></td><td>{len(l.get_travel_list())}</td></tr>'
            f'<tr><td><a href="/airlinepage/">Авиаперевозчики</a></td><td>{len(l.get_airline_list())}</td></tr>'
            f'<tr><td><a href="/touroperatorpage/">Туроператоры</a></td><td>{len(l.get_tour_operator_list())}</td></tr>'
            f'<tr><td><a href="/managerpage/">Менеджеры</a></td><td>{len(l.get_manager_list())}</td></tr>'
            f'<tr><td><a href="/paymentpage/">Платежи</a></td><td>{len(l.get_payment_list())}</td></tr>'
            f'</table>'
        )
        body = (
            f'<p>Загружено: <code>{esc(self.__fname)}</code> '
            f'(формат {esc(self.__fmt)})</p>'
            + summary
            + '<h3>Сохранить</h3>'
            + self._save_form()
            + '<h3>Открыть другой файл</h3>'
            + self._open_form('', 'JSON', loaded=True)
        )
        return page('Турфирма — главная', body)
    index.exposed = True

    def openfile(self, fname='', dformat=''):
        if not fname:
            return page('Ошибка', '<p>Не указано имя файла.</p>' + back_link('/'))
        try:
            self.__lib.clear()
            fmt = _detect_format(fname, dformat)
            obj = self._serializer_for(fmt)
            if obj is None:
                raise ValueError(f'Неизвестный формат: {fmt!r}')
            obj.set_inp(fname)
            obj.read()
            self.__loaded = True
            self.__fname = fname
            self.__fmt = fmt
            return page('Готово',
                        f'<p>Данные загружены из <code>{esc(fname)}</code> '
                        f'(формат {esc(fmt)}).</p>' + back_link('/'))
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link('/'))
    openfile.exposed = True

    def savefile(self, fname='', dformat=''):
        if not fname:
            return page('Ошибка', '<p>Не указано имя файла.</p>' + back_link('/'))
        try:
            fmt = _detect_format(fname, dformat)
            obj = self._serializer_for(fmt)
            if obj is None:
                raise ValueError(f'Неизвестный формат: {fmt!r}')
            if fmt == 'SQL' and os.path.isfile(fname):
                os.remove(fname)
            obj.set_out(fname)
            obj.write()
            return page('Готово',
                        f'<p>Сохранено в <code>{esc(fname)}</code> '
                        f'(формат {esc(fmt)}).</p>' + back_link('/'))
        except Exception as e:
            return page('Ошибка', f'<p>{esc(e)}</p>' + back_link('/'))
    savefile.exposed = True

    def _serializer_for(self, fmt):
        if fmt == 'JSON':
            return self.__djson
        if fmt == 'XML':
            return self.__dxml
        if fmt == 'SQL':
            return self.__dsql
        return None

    def _open_form(self, default_name, default_fmt, loaded=False):
        opts = ''.join(
            f'<option value="{f}"{" selected" if f == default_fmt else ""}>{f}</option>'
            for f in ('JSON', 'XML', 'SQL')
        )
        return f'''
<form action="/openfile" method="post">
<table>
<tr><td>Файл:</td><td><input name="fname" value="{esc(default_name)}" size="40"></td></tr>
<tr><td>Формат:</td><td><select name="dformat">{opts}</select></td></tr>
<tr><td colspan="2"><input type="submit" value="Открыть"></td></tr>
</table>
</form>'''

    def _save_form(self):
        fmts = ('JSON', 'XML', 'SQL')
        opts = ''.join(
            f'<option value="{f}"{" selected" if f == self.__fmt else ""}>{f}</option>'
            for f in fmts
        )
        return f'''
<form action="/savefile" method="post">
<table>
<tr><td>Файл:</td><td><input name="fname" value="{esc(self.__fname)}" size="40"></td></tr>
<tr><td>Формат:</td><td><select name="dformat">{opts}</select></td></tr>
<tr><td colspan="2"><input type="submit" value="Сохранить"></td></tr>
</table>
</form>'''


if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080,
    })
    cherrypy.quickstart(Root(), '/')
