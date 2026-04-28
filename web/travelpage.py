import cherrypy

class travelpage:

    def __init__(self, library):
        self.__lib = library

    def index(self):
        s = '<a href="../">назад</a> / <a href="addform">добавить путёвку</a><br><br>\n<table border="1" cellpadding="5" cellspacing="0">\n<tr bgcolor="gray">\n<th>№</th><th>Код</th><th>Дата</th><th>Кол-во</th><th>Скидка %</th><th>Клиенты</th><th>Маршруты</th><th>Действия</th>\n</tr>'
        r = 1
        bg = ''
        for t in self.__lib.getTravelList():
            code = t.getCode()
            clients_str = ', '.join(map(str, t.getClientCodes())) or '—'
            routes_str = ', '.join(map(str, t.getRouteCodes())) or '—'
            s += f'<tr{bg}><td>{r}</td><td>{code}</td>'
            s += f"<td>{t.getDate() or ''}</td><td>{t.getQuantity()}</td><td>{t.getDiscount()}</td>"
            s += f'<td>{clients_str}</td><td>{routes_str}</td>'
            s += f'<td><a href="editform?code={code}">редактировать</a> | '
            s += f'<a href="delr?code={code}">удалить</a></td></tr>'
            r += 1
            bg = '' if bg else ' bgcolor="silver"'
        s += '</table>'
        return s
    index.exposed = True

    def addform(self):
        clients = self.__lib.getClientList()
        routes = self.__lib.getRouteList()
        s = 'Добавить путёвку<br><br>\n<form action="addaction" method="post">\n<table border="0">\n<tr><td>Дата отправления:</td><td><input type="text" name="date" placeholder="" size="20"></td></tr>\n<tr><td>Количество человек:</td><td><input type="number" name="quantity" value="1" min="1"></td></tr>\n<tr><td>Скидка (%):</td><td><input type="number" name="discount" value="0" min="0" max="100"></td></tr>\n</table>\n\n<h3>Клиенты (удерживайте Ctrl для множественного выбора):</h3>\n<select name="clients" multiple size="8" style="width:450px">'
        for c in clients:
            s += f'<option value="{c.getCode()}">{c.getSurname()} {c.getName()} {c.getSecname()} (код {c.getCode()})</option>'
        s += '</select><br><br>'
        s += '<h3>Маршруты (удерживайте Ctrl для множественного выбора):</h3>\n<select name="routes" multiple size="8" style="width:450px">'
        for rt in routes:
            s += f'<option value="{rt.getCode()}">{rt.getName()} — {rt.getHotel()} ({rt.getDuration()} дней)</option>'
        s += '</select><br><br>'
        s += '<input type="submit" value="Добавить путёвку">\n</form><br>\n<a href="index">назад к списку</a>'
        return s
    addform.exposed = True

    def addaction(self, date='', quantity=1, discount=0, clients=None, routes=None):
        try:
            if clients is None:
                clients = []
            if routes is None:
                routes = []
            if isinstance(clients, str):
                clients = [clients]
            if isinstance(routes, str):
                routes = [routes]
            code = self.__lib.getTravelNewCode()
            travel = self.__lib.createTravel(code, date.strip(), int(quantity), int(discount))
            for cl_code in clients:
                travel.appendClient(int(cl_code))
            for rt_code in routes:
                travel.appendRoute(int(rt_code))
            return f"Путёвка №{code} успешно добавлена<br><a href='index'>назад к списку</a>"
        except Exception as e:
            return f"Ошибка добавления: {e}<br><a href='addform'>назад</a>"
    addaction.exposed = True

    def editform(self, code=0):
        try:
            t = self.__lib.getTravel(int(code))
            all_clients = self.__lib.getClientList()
            all_routes = self.__lib.getRouteList()
            selected_clients = set(t.getClientCodes())
            selected_routes = set(t.getRouteCodes())
            s = f'''Редактировать путёвку №{code}<br><br>\n<form action="editaction" method="post">\n<input type="hidden" name="code" value="{code}">\n\n<table border="0">\n<tr><td>Дата отправления:</td><td><input type="text" name="date" value="{t.getDate() or ''}" size="20"></td></tr>\n<tr><td>Количество человек:</td><td><input type="number" name="quantity" value="{t.getQuantity()}" min="1"></td></tr>\n<tr><td>Скидка (%):</td><td><input type="number" name="discount" value="{t.getDiscount()}" min="0" max="100"></td></tr>\n</table>\n\n<h3>Клиенты (удерживайте Ctrl):</h3>\n<select name="clients" multiple size="8" style="width:450px">'''
            for c in all_clients:
                sel = ' selected' if c.getCode() in selected_clients else ''
                s += f'<option value="{c.getCode()}"{sel}>{c.getSurname()} {c.getName()} {c.getSecname()} (код {c.getCode()})</option>'
            s += '</select><br><br>'
            s += '<h3>Маршруты (удерживайте Ctrl):</h3>\n<select name="routes" multiple size="8" style="width:450px">'
            for rt in all_routes:
                sel = ' selected' if rt.getCode() in selected_routes else ''
                s += f'<option value="{rt.getCode()}"{sel}>{rt.getName()} — {rt.getHotel()} ({rt.getDuration()} дней)</option>'
            s += '</select><br><br>'
            s += '<input type="submit" value="Сохранить изменения">\n</form><br>\n<a href="index">назад к списку</a>'
            return s
        except Exception as e:
            return f"Ошибка загрузки путёвки: {e}<br><a href='index'>назад</a>"
    editform.exposed = True

    def editaction(self, code=0, date='', quantity=1, discount=0, clients=None, routes=None):
        try:
            if clients is None:
                clients = []
            if routes is None:
                routes = []
            if isinstance(clients, str):
                clients = [clients]
            if isinstance(routes, str):
                routes = [routes]
            code = int(code)
            self.__lib.removeTravel(code)
            travel = self.__lib.createTravel(code, date.strip(), int(quantity), int(discount))
            for cl_code in clients:
                travel.appendClient(int(cl_code))
            for rt_code in routes:
                travel.appendRoute(int(rt_code))
            return f"Путёвка №{code} успешно обновлена<br><a href='index'>назад к списку</a>"
        except Exception as e:
            return f"Ошибка сохранения: {e}<br><a href='index'>назад</a>"
    editaction.exposed = True

    def delr(self, code=0):
        try:
            self.__lib.removeTravel(int(code))
            return f"Путёвка №{code} удалена<br><a href='index'>назад</a>"
        except:
            return "Ошибка удаления<br><a href='index'>назад</a>"
    delr.exposed = True
